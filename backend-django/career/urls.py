from django.urls import path

from .views import (
    DashboardView,
    ExamsView,
    InterviewGenerateQuestionsView,
    InterviewSubmitAnswerView,
    ProfileView,
    ResumeAnalysisView,
    ResumeUploadView,
)

urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("resume/upload/", ResumeUploadView.as_view(), name="resume-upload"),
    path("resume/analysis/", ResumeAnalysisView.as_view(), name="resume-analysis"),
    path("interview/generate-questions/", InterviewGenerateQuestionsView.as_view(), name="interview-generate-questions"),
    path("interview/submit-answer/", InterviewSubmitAnswerView.as_view(), name="interview-submit-answer"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("exams/", ExamsView.as_view(), name="exams"),
]
