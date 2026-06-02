from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    EXPERIENCE_CHOICES = [
        ("fresher", "Fresher"),
        ("entry", "Entry Level"),
        ("mid", "Mid Level"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="career_profile")
    name = models.CharField(max_length=120)
    skills = models.JSONField(default=list, blank=True)
    education = models.CharField(max_length=200, blank=True)
    target_role = models.CharField(max_length=120, blank=True)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default="fresher")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Resume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resumes")
    file = models.FileField(upload_to="resumes/")
    extracted_text = models.TextField(blank=True)
    score = models.PositiveSmallIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email or self.user.username} resume"


class AIFeedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ai_feedback")
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="feedback", null=True, blank=True)
    target_role = models.CharField(max_length=120, blank=True)
    resume_score = models.PositiveSmallIntegerField(default=0)
    strengths = models.JSONField(default=list, blank=True)
    weaknesses = models.JSONField(default=list, blank=True)
    missing_skills = models.JSONField(default=list, blank=True)
    suggested_improvements = models.JSONField(default=list, blank=True)
    interview_questions = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AI feedback for {self.user.username}"


class InterviewSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="interview_sessions")
    exam_id = models.CharField(max_length=40, blank=True)
    job_role = models.CharField(max_length=120)
    questions = models.JSONField(default=list)
    answers = models.JSONField(default=list, blank=True)
    feedback = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.job_role} interview for {self.user.username}"


class SkillProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="skill_progress")
    exam_id = models.CharField(max_length=40)
    skill_name = models.CharField(max_length=100)
    progress_percent = models.PositiveSmallIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "exam_id", "skill_name")

    def __str__(self):
        return f"{self.skill_name}: {self.progress_percent}%"
