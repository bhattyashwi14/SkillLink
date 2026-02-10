from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class TutorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tutor_profile')
    bio = models.TextField(max_length=500, blank=True)
    profile_pic = models.ImageField(upload_to='tutor_pics/', null=True, blank=True)
    
    # Skills Many-to-Many

    # Skills Many-to-Many
    skills = models.ManyToManyField(Skill, blank=True)

    # Teaching Skills (Text Input)
    teaching_skills = models.TextField(max_length=500, blank=True, null=True)

    

    # Verification & Stats
    proof_of_skill = models.FileField(upload_to='tutor_proofs/', null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    total_students = models.IntegerField(default=0)
    github_profile = models.URLField(max_length=255, blank=True, null=True)
    linkedin_profile = models.URLField(max_length=255, blank=True, null=True)
    rating = models.FloatField(default=0.0)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)


    def __str__(self):
        return f"{self.user.username}'s Tutor Profile"

class Availability(models.Model):
    DAYS = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    tutor = models.ForeignKey(TutorProfile, on_delete=models.CASCADE, related_name='availabilities')
    day_of_week = models.CharField(max_length=10, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        verbose_name_plural = "Availabilities"

class Booking(models.Model):
    tutor = models.ForeignKey(
        TutorProfile,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="student_bookings"
    )

    availability = models.ForeignKey(
        Availability,
        on_delete=models.CASCADE
    )

    booked_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ("booked", "Booked"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="booked"
    )

    def __str__(self):
        return f"{self.student.username} → {self.tutor.user.username} ({self.availability.day_of_week})"

