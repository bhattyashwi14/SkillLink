from django.contrib import admin

# Register your models here.

from .models import ClientProfile, TutorProfile, JobPost, JobApplication, Notification , HiringRequest

admin.site.register(ClientProfile)
admin.site.register(TutorProfile)
admin.site.register(JobPost)
admin.site.register(JobApplication)
admin.site.register(Notification)
admin.site.register(HiringRequest)
