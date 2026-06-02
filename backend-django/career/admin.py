from django.contrib import admin

from .models import AIFeedback, InterviewSession, Resume, SkillProgress, UserProfile


admin.site.register(UserProfile)
admin.site.register(Resume)
admin.site.register(AIFeedback)
admin.site.register(InterviewSession)
admin.site.register(SkillProgress)
