from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Resume",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("file", models.FileField(upload_to="resumes/")),
                ("extracted_text", models.TextField(blank=True)),
                ("score", models.PositiveSmallIntegerField(default=0)),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="resumes", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("skills", models.JSONField(blank=True, default=list)),
                ("education", models.CharField(blank=True, max_length=200)),
                ("target_role", models.CharField(blank=True, max_length=120)),
                ("experience_level", models.CharField(choices=[("fresher", "Fresher"), ("entry", "Entry Level"), ("mid", "Mid Level")], default="fresher", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="career_profile", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="SkillProgress",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("exam_id", models.CharField(max_length=40)),
                ("skill_name", models.CharField(max_length=100)),
                ("progress_percent", models.PositiveSmallIntegerField(default=0)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="skill_progress", to=settings.AUTH_USER_MODEL)),
            ],
            options={"unique_together": {("user", "exam_id", "skill_name")}},
        ),
        migrations.CreateModel(
            name="InterviewSession",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("exam_id", models.CharField(blank=True, max_length=40)),
                ("job_role", models.CharField(max_length=120)),
                ("questions", models.JSONField(default=list)),
                ("answers", models.JSONField(blank=True, default=list)),
                ("feedback", models.TextField(blank=True)),
                ("completed", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="interview_sessions", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="AIFeedback",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("target_role", models.CharField(blank=True, max_length=120)),
                ("resume_score", models.PositiveSmallIntegerField(default=0)),
                ("strengths", models.JSONField(blank=True, default=list)),
                ("weaknesses", models.JSONField(blank=True, default=list)),
                ("missing_skills", models.JSONField(blank=True, default=list)),
                ("suggested_improvements", models.JSONField(blank=True, default=list)),
                ("interview_questions", models.JSONField(blank=True, default=list)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("resume", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="feedback", to="career.resume")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="ai_feedback", to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
