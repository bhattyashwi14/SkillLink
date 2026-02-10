from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_TYPES = (
        ('student', 'Student'),
        ('tutor', 'Tutor'),
        ('company', 'Company'),
    )
    
    # user = models.OneToOneField(User, on_register=True, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='student')
    bio = models.TextField(blank=True)
    
    # Data Science ready fields
    # Stored as "Python, Django, SQL"
    skills = models.TextField(help_text="Enter skills separated by commas", blank=True)
    
    # Stored for Matplotlib visualization
    rating = models.FloatField(default=0.0)
    total_reviews = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

    def get_skills_list(self):
        return [s.strip() for s in self.skills.split(',')]
    

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100, blank=True)
    semester = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)
    skills = models.TextField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)

    profile_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email