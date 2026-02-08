from django.contrib import admin

# Register your models here.
from .models import Skill, TutorProfile, Availability

# Register your models here.
admin.site.register(Skill)
admin.site.register(TutorProfile)
admin.site.register(Availability)