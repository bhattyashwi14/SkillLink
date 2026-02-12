from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# class ClientProfile(models.Model):

#     user = models.OneToOneField(User, on_delete=models.CASCADE)

#     client_id = models.CharField(
#         max_length=10,
#         unique=True,
#         blank=True
#     )

#     work_proof = models.FileField(upload_to="work_proofs/", null=True, blank=True)

#     is_verified = models.BooleanField(default=False)

#     def save(self, *args, **kwargs):

#         if not self.client_id:
#             last = ClientProfile.objects.order_by("id").last()

#             if last:
#                 number = int(last.client_id[1:]) + 1
#             else:
#                 number = 1

#             self.client_id = f"C{number:04d}"  
#             # C0001 format

#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.client_id
class ClientProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    client_id = models.CharField(
        max_length=10,
        unique=True,
        blank=True
    )

    company_name = models.CharField(max_length=255)

    location = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    bio = models.TextField(
        blank=True,
        null=True
    )

    linkedin = models.URLField(
        blank=True,
        null=True
    )

    work_proof = models.FileField(
        upload_to="work_proofs/",
        null=True,
        blank=True
    )

    is_verified = models.BooleanField(default=False)

    is_profile_complete = models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        if not self.client_id:
            last = ClientProfile.objects.order_by('id').last()

            if last:
                number = int(last.client_id[1:]) + 1
            else:
                number = 1

            self.client_id = f"C{number:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.client_id


class EmailOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=now)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.otp}"
    
class TutorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.TextField()
    experience = models.CharField(max_length=100)
    resume = models.FileField(upload_to='tutor_resumes/', blank=True, null=True)
    portfolio_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    #

    def __str__(self):
        return self.user.username

class JobPost(models.Model):
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    skills_required = models.TextField()
    job_type = models.CharField(
        max_length=50,
        choices=[
            ('Full-time', 'Full-time'),
            ('Part-time', 'Part-time'),
            ('Internship', 'Internship'),
            ('Freelance', 'Freelance')
        ]
    )
    location = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class JobApplication(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50,
        choices=[
            ('Pending', 'Pending'),
            ('Shortlisted', 'Shortlisted'),
            ('Rejected', 'Rejected'),
            ('Hired', 'Hired')
        ],
        default='Pending'
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tutor.username} - {self.job.title}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)



class HiringRequest(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    status = models.CharField(
    max_length=10,
    choices=STATUS_CHOICES,
    default="pending"
)

    MODE_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_hiring_requests'
    )

    tutor = models.ForeignKey(
        'TutorProfile',
        on_delete=models.CASCADE,
        related_name='received_hiring_requests'
    )

    skill = models.CharField(max_length=100)

    budget = models.PositiveIntegerField()

    duration = models.CharField(max_length=100)

    mode = models.CharField(
        max_length=10,
        choices=MODE_CHOICES
    )

    description = models.TextField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client} → {self.tutor} ({self.status})"
