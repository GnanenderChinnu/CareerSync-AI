from django.db.models import Avg
from rest_framework import parsers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .exam_content import EXAMS
from .models import AIFeedback, InterviewSession, Resume, SkillProgress, UserProfile
from .serializers import AIFeedbackSerializer, ResumeSerializer, UserProfileSerializer
from .services import analyze_career_readiness, generate_interview_questions


class ProfileView(APIView):
    def get(self, request):
        profile, _ = UserProfile.objects.get_or_create(
            user=request.user,
            defaults={"name": request.user.first_name or request.user.username},
        )
        return Response(UserProfileSerializer(profile).data)

    def post(self, request):
        profile, _ = UserProfile.objects.get_or_create(
            user=request.user,
            defaults={"name": request.user.first_name or request.user.username},
        )
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ResumeUploadView(APIView):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def post(self, request):
        serializer = ResumeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resume = serializer.save(user=request.user)
        profile = getattr(request.user, "career_profile", None)
        analysis = analyze_career_readiness(
            resume_text=resume.extracted_text,
            target_role=profile.target_role if profile else "",
            user_skills=profile.skills if profile else [],
        )
        resume.score = analysis["resume_score"]
        resume.save(update_fields=["score"])
        AIFeedback.objects.create(
            user=request.user,
            resume=resume,
            target_role=profile.target_role if profile else "",
            **analysis,
        )
        return Response(ResumeSerializer(resume).data, status=status.HTTP_201_CREATED)


class ResumeAnalysisView(APIView):
    def get(self, request):
        feedback = AIFeedback.objects.filter(user=request.user).order_by("-created_at").first()
        if not feedback:
            profile = getattr(request.user, "career_profile", None)
            analysis = analyze_career_readiness(
                target_role=profile.target_role if profile else "",
                user_skills=profile.skills if profile else [],
            )
            feedback = AIFeedback.objects.create(user=request.user, target_role=analysis.get("target_role", ""), **analysis)
        return Response(AIFeedbackSerializer(feedback).data)


class InterviewGenerateQuestionsView(APIView):
    def post(self, request):
        job_role = request.data.get("job_role", "IT Associate")
        exam_id = request.data.get("exam_id", "")
        profile = getattr(request.user, "career_profile", None)
        questions = generate_interview_questions(job_role, profile.skills if profile else [], exam_id)
        session = InterviewSession.objects.create(
            user=request.user,
            exam_id=exam_id,
            job_role=job_role,
            questions=questions,
        )
        return Response({"session_id": session.id, "questions": questions}, status=status.HTTP_201_CREATED)


class InterviewSubmitAnswerView(APIView):
    def post(self, request):
        session_id = request.data.get("session_id")
        answer = request.data.get("answer", "")
        if not session_id or not answer:
            return Response({"detail": "session_id and answer are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            session = InterviewSession.objects.get(id=session_id, user=request.user)
        except InterviewSession.DoesNotExist:
            return Response({"detail": "Interview session not found."}, status=status.HTTP_404_NOT_FOUND)
        answers = session.answers or []
        answers.append(answer)
        session.answers = answers
        session.completed = len(answers) >= len(session.questions)
        session.feedback = "Good start. Add more structure, examples, and measurable outcomes in your answers."
        session.save()
        return Response({"completed": session.completed, "feedback": session.feedback})


class DashboardView(APIView):
    def get(self, request):
        latest_resume = Resume.objects.filter(user=request.user).order_by("-uploaded_at").first()
        completed_interviews = InterviewSession.objects.filter(user=request.user, completed=True).count()
        skills = SkillProgress.objects.filter(user=request.user)
        progress = skills.aggregate(avg=Avg("progress_percent"))["avg"] or 38
        latest_feedback = AIFeedback.objects.filter(user=request.user).order_by("-created_at").first()

        return Response(
            {
                "resume_score": latest_resume.score if latest_resume else 72,
                "completed_mock_interviews": completed_interviews,
                "skills_to_improve": latest_feedback.missing_skills if latest_feedback else ["SQL", "Data Structures", "Communication"],
                "progress_percentage": round(progress),
                "recommended_exams": EXAMS,
            }
        )


class ExamsView(APIView):
    def get(self, request):
        return Response(EXAMS)
