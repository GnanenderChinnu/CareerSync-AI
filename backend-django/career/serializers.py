from rest_framework import serializers

from .models import AIFeedback, InterviewSession, Resume, SkillProgress, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["name", "skills", "education", "target_role", "experience_level", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ["id", "file", "extracted_text", "score", "uploaded_at"]
        read_only_fields = ["id", "score", "uploaded_at"]


class AIFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIFeedback
        fields = [
            "id",
            "target_role",
            "resume_score",
            "strengths",
            "weaknesses",
            "missing_skills",
            "suggested_improvements",
            "interview_questions",
            "created_at",
        ]


class InterviewSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewSession
        fields = ["id", "exam_id", "job_role", "questions", "answers", "feedback", "completed", "created_at"]
        read_only_fields = ["id", "questions", "feedback", "completed", "created_at"]


class SkillProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillProgress
        fields = ["exam_id", "skill_name", "progress_percent", "updated_at"]
