from django.contrib import admin
from .models import Skill, TutorProfile, Availability
from .models import Booking

admin.site.register(Booking)



@admin.register(TutorProfile)
class TutorProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "is_approved",
        "rating",
        "total_students"
    )
    list_editable = ("is_approved",)


admin.site.register(Skill)

admin.site.register(Availability)



class TutorProfileAdmin(admin.ModelAdmin):
    # This displays the columns in the list view
    list_display = ('user', 'is_approved', 'total_students', 'rating')
    
    # This allows you to search by username
    search_fields = ('user__username',)

# Register the other models so you can see them too

