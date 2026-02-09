from django.contrib import admin

# Register your models here.
from .models import Skill, TutorProfile, Availability

# Register your models here.
admin.site.register(Skill)
admin.site.register(TutorProfile)
admin.site.register(Availability)



class TutorProfileAdmin(admin.ModelAdmin):
    # This displays the columns in the list view
    list_display = ('user', 'is_approved', 'total_students', 'rating')
    
    # This allows you to search by username
    search_fields = ('user__username',)

# Register the other models so you can see them too
