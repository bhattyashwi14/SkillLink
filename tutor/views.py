from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from core.models import Profile
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib import messages
import random
from .models import TutorProfile, Skill, Availability
from .models import Booking
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Booking, Availability
import uuid
from django.http import HttpResponse




# ======================================================================================

# Create your views here.
def tutor_auth(request):
    return render(request, 'tutor/tutor_auth.html')


# def tutor_register(request):
#     if request.method == 'POST':
#         data = request.POST
#         uname = data.get('username')
#         uemail = data.get('email')
#         upass = data.get('password')
#         uconfirm = data.get('confirm_password')
# ======================================================================================
        # if upass != uconfirm:
        #     return render(request, 'tutor/tutor_auth.html', {
        #         'password_error': "Passwords do not match!"
        #     })
        #     # messages.error(request, "Passwords do not match!")
        # if not (uemail.endswith("@gmail.com") or uemail.endswith("@yahoo.com") or uemail.endswith("@icloud.com")):
        #     # return render(request, 'tutor/tutor_auth.html')
        #     return render(request, 'tutor/tutor_auth.html', {
        #         'email_error': "Invalid email extension!",
        #         'typed_email': uemail
        #     })
# ======================================================================================
        
    #     if upass != uconfirm:
    #         return render(request, 'tutor/tutor_auth.html', {
    #             'password_error': "Passwords do not match!",
    #             'typed_name': uname,
    #             'typed_email': uemail,
    #             'register_error': True
    #         })

    #     valid_extensions = ("@gmail.com", "@yahoo.com", "@icloud.com")
    #     if not uemail.lower().endswith(valid_extensions):
    #         return render(request, 'tutor/tutor_auth.html', {
    #             'email_error': "Invalid email!",
    #             'typed_name': uname,
    #             'typed_email': uemail,
    #             'register_error': True
    #         })

        
    #     special_chars = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
    #     has_special = any(char in special_chars for char in upass)
    #     has_number = any(char.isdigit() for char in upass)

    #     if len(upass) < 8 or not has_special or not has_number:
    #         return render(request, 'tutor/tutor_auth.html', {
    #             'password_error': "Password needs 8+ chars, a number, and a special char!",
    #             'typed_name': uname,
    #             'typed_email': uemail,
    #             'register_error': True
    #         })
        
    #     if User.objects.filter(username=uname).exists():
    #         return render(request, 'tutor/tutor_auth.html', {'name_error': "Username taken!"})

    #     new_user = User.objects.create_user(username=uname, email=uemail, password=upass)
    #     Profile.objects.create(user=new_user, user_type='tutor')
        
    #     return redirect('login')
        
    # return render(request, 'tutor/tutor_auth.html')
# ======================================================================================

            # if not re.match(email_pattern, uemail):
        #     messages.error(request, "Invalid email format or provider!")
        #     return render(request, 'tutor/tutor_auth.html')

        # special_chars = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        # has_special = any(char in special_chars for char in upass)
        # has_number = any(char.isdigit() for char in upass)

        # if len(upass) < 8 or not has_special or not has_number:
        #     messages.error(request, "Password must be 8+ chars with a number and special char!")
        #     return render(request, 'tutor/tutor_auth.html')

        # if User.objects.filter(username=uname).exists():
        #     messages.error(request, "Username already taken!")
        #     return render(request, 'tutor/tutor_auth.html')

        # new_user = User.objects.create_user(username=uname, email=uemail, password=upass)
        
        # Profile.objects.create(user=new_user, user_type='tutor')



# ==============================
# TUTOR LOGIN ENTRY (mode based)
# ==============================
# def tutor_login(request):
#     mode = request.GET.get("mode")

#     if mode == "login":
#         print("tutorlogin login mode")
#         return tutor_login_form(request)

#     if mode == "signup":
#         print("tutorlogin signup mode")
#         return tutor_register(request)

#     return render(request, "tutor/tutor_auth.html")


# ==============================
# LOGIN FORM
# ==============================
def tutor_login_form(request):

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, "tutor/login.html", {
                "email_error": "No tutor account found with this email",
                "email": email
            })

        # Authenticate
        user = authenticate(request, username=user.username, password=password)

        if user is None:
            return render(request, "tutor/login.html", {
                "pass_error": "Incorrect password",
                "email": email
            })

        # Check if user is tutor
        if not hasattr(user, "profile") or user.profile.user_type != "tutor":
            return render(request, "tutor/login.html", {
                "email_error": "This account is not registered as tutor"
            })

        login(request, user)

        # If profile already has slots, go to dashboard
        try:
            profile = user.tutor_profile
            if profile.availabilities.exists():
                return redirect("tutor:tutor_dashboard")
        except:
            pass

        return redirect("tutor:complete_profile")

        # print("login successfull!")
    return render(request, "tutor/login.html")


# ==============================
# TUTOR REGISTER WITH OTP
# ==============================
def tutor_register(request):
    action = request.POST.get("action")

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        otp = request.POST.get("otp")

        # EMAIL VALIDATION
        valid_extensions = (
            "@gmail.com", "@yahoo.com", "@icloud.com",
            "@outlook.com", "@hotmail.com"
        )

        if not email.lower().endswith(valid_extensions):
            return render(request, "tutor/signup.html", {
                "email_error": "Invalid email provider",
                "email": email
            })

        if User.objects.filter(email=email).exists():
            return render(request, "tutor/signup.html", {
                "email_error": "Email already registered",
                "email": email
            })

        # ======================
        # STEP 1 — SEND OTP
        # ======================
        if action == "send_otp":

            generated_otp = otp_generation()
            request.session["otp"] = str(generated_otp)
            request.session["reg_email"] = email

            send_mail(
                "SkillLink Tutor OTP",
                f"Your OTP is: {generated_otp}",
                "skill.link.connects@gmail.com",
                [email],
            )

            return render(request, "tutor/signup.html", {
                "email": email,
                "show_otp": True,
                "info": "OTP sent successfully"
            })

        # ======================
        # STEP 2 — VERIFY OTP
        # ======================
        if action == "verify_otp":

            session_otp = request.session.get("otp")

            if not session_otp or otp != session_otp:
                return render(request, "tutor/signup.html", {
                    "email": email,
                    "show_otp": True,
                    "otp_error": "Incorrect OTP",
                    "otp": otp
                })


            return render(request, "tutor/signup.html", {
                "email": email,
                "show_otp": True,
                "show_password": True,
                "otp_success": "OTP verified"
            })

        # ======================
        # STEP 3 — CREATE ACCOUNT
        # ======================
        if action == "create_account":

            if password != confirm_password:
                return render(request, "tutor/signup.html", {
                    "email": email,
                    "show_otp": True,
                    "show_password": True,
                    "match_error": "Passwords do not match"
                })

            # Strong password check
            if len(password) < 8:
                return render(request, "tutor/signup.html", {
                    "email": email,
                    "show_otp": True,
                    "show_password": True,
                    "pass_error": "Password must be at least 8 characters"
                })

            # Create username from email
            username = email.split("@")[0]

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            Profile.objects.create(
                user=user,
                user_type="tutor"
            )

            # Clean session
            request.session.pop("otp", None)
            request.session.pop("reg_email", None)
            # print("account creayed successfully!")
            login(request, user)

            return redirect("tutor:complete_profile")
    return render(request, "tutor/signup.html", {
        "show_otp": False,
        "show_password": False
    })


# # ==============================
# # DASHBOARD
# # ==============================
# # def tutor_dashboard(request):

# #     if not request.user.is_authenticated:
# #         return redirect("tutor_login")

# #     if request.user.profile.user_type != "tutor":
# #         return redirect("tutor_login")

# #     return render(request, "tutor/tutor_dashboard.html")


# # ==============================
# # LOGOUT
# # ==============================
# # def tutor_logout(request):
# #     logout(request)
# #     return redirect("tutor_login")


# ==============================
# OTP GENERATION
# ==============================
def otp_generation():
    return random.randint(100000, 999999)

def tutor_dashboard(request):
    
    try:
        profile = request.user.tutor_profile
    except TutorProfile.DoesNotExist:
        return redirect('tutor:complete_profile')
        
    # ALL slots created by tutor
    all_slots = profile.availabilities.all()

    # Booked slot IDs
    booked_slot_ids = Booking.objects.filter(
        tutor=profile
    ).values_list("availability_id", flat=True)

    # 1️⃣ Editable Slots (Not Booked)
    editable_slots = all_slots.exclude(id__in=booked_slot_ids)

    # 2️⃣ Booked Slots (Active)
    active_bookings = Booking.objects.filter(
        tutor=profile,
        status="booked"  # adjust if needed
    ).select_related("student", "availability").order_by("-booked_at")

    # 3️⃣ Completed Sessions
    completed_sessions = Booking.objects.filter(
        tutor=profile,
        status="completed"
    ).select_related("student", "availability").order_by("-booked_at")


    # ✅ ADD THIS BLOCK
    pending_count = HiringRequest.objects.filter(
        tutor=profile,
        status='pending'
    ).count()

    selected_skills = list(profile.skills.values_list("name", flat=True))

    return render(request, "tutor/tutor_dashboard.html", {
        "profile": profile,
        "editable_slots": editable_slots,
        "active_bookings": active_bookings,
        "completed_sessions": completed_sessions,
        "pending_count": pending_count,
        "selected_skills": selected_skills,
    })


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def complete_profile(request):

    if request.user.profile.user_type != "tutor":
        return redirect("login")

    profile, created = TutorProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":

        # ===== BASIC INFO =====
        full_name = request.POST.get("full_name")
        profile.bio = request.POST.get("bio")
        profile.linkedin_profile = request.POST.get("linkedin_profile")
        profile.github_profile = request.POST.get("github_profile")
        profile.teaching_skills = request.POST.get("tutoring_skills")

        if full_name:
            request.user.first_name = full_name
            request.user.save()

        if request.FILES.get("proof_file"):
            profile.proof_of_skill = request.FILES.get("proof_file")

        profile.save()

        # ===== TECHNICAL SKILLS (CLIENT SIDE) =====
        skill_names = request.POST.getlist("skills")
        other_skills = request.POST.get("other_skills")

        # Add newly typed skills to the checked list
        if other_skills:
            extra = [s.strip() for s in other_skills.split(",") if s.strip()]
            skill_names.extend(extra)

        # Clear all skills first
        profile.skills.clear()

        # Add only the checked + newly added ones
        for name in skill_names:
            skill_obj, _ = Skill.objects.get_or_create(name=name)
            profile.skills.add(skill_obj)


        # ===== SESSION SLOTS (LEARNER SIDE) =====
        # ===== MULTIPLE SLOT HANDLING =====

        slot_skills = request.POST.getlist("slot_skill")
        slot_dates = request.POST.getlist("slot_date")
        slot_starts = request.POST.getlist("slot_start")
        slot_ends = request.POST.getlist("slot_end")

        for i in range(len(slot_skills)):

            skill_name = slot_skills[i].strip()

            if skill_name:
                Availability.objects.create(
                    tutor=profile,
                    skill_name=skill_name,
                    date=slot_dates[i],
                    start_time=slot_starts[i],
                    end_time=slot_ends[i]
                )

        messages.success(request, "Profile updated successfully!")
        return redirect("tutor:tutor_dashboard")

    return render(request, "tutor/complete_profile.html", {
        "profile": profile
    })


# =================================================================================
# =================================================================================

# @login_required
# def complete_profile(request):
#     profile = getattr(request.user, 'tutor_profile', None)
#     if profile and profile.bio: # Using bio as a check for 'completeness'
#         return redirect('tutor_dashboard')
#     # Use the related_name 'tutor_profile' from your model
#     # This ensures a profile object exists for the current user
#     profile, created = TutorProfile.objects.get_or_create(user=request.user)

#     if request.method == "POST":
#         # 1. Update Basic Info
#         full_name = request.POST.get("full_name")
#         profile.bio = request.POST.get("bio")
#         profile.github_profile = request.POST.get("github") # Ensure name matches your HTML input name
#         profile.linkedin_profile = request.POST.get("linkedin")
#         profile.teaching_skills = request.POST.get("tutoring_skills")
#         # Update User model first_name
#         if full_name:
#             request.user.first_name = full_name
#             request.user.save()

#         # 2. Handle File Uploads
#         if request.FILES.get("proof_file"):
#             profile.proof_of_skill = request.FILES.get("proof_file")
#         if request.FILES.get("profile_pic"):
#             profile.profile_pic = request.FILES.get("profile_pic")
        

#         profile.save()

#         # 3. Handle Skills (ManyToManyField)
#         # request.POST.getlist grabs ALL checked values
#         skill_names = request.POST.getlist("skills")
#         other_skills = request.POST.get("other_skills")
        
#         if other_skills:
#             extra_skills = [s.strip() for s in other_skills.split(",") if s.strip()]
#             skill_names.extend(extra_skills)

#         # Clear existing skills and re-add (prevents duplicates)
#         profile.skills.clear()
#         for name in skill_names:
#             skill_obj, _ = Skill.objects.get_or_create(name=name)
#             profile.skills.add(skill_obj)

#         # 4. Handle Availability (ForeignKey)
#         selected_days = request.POST.getlist("available_days")
#         start_t = request.POST.get("start_time")
#         end_t = request.POST.get("end_time")

#         if selected_days and start_t and end_t:
#             # Delete old ones to avoid messy data
#             Availability.objects.filter(tutor=profile).delete()
#             for day in selected_days:
#                 Availability.objects.create(
#                     tutor=profile,
#                     day_of_week=day,
#                     start_time=start_t,
#                     end_time=end_t
#                 )

#         return redirect("tutor_dashboard")

#     return render(request, "tutor/complete_profile.html")# from django.shortcuts import render,redirect
# =================================================================================
# =================================================================================

    return render(request, "tutor/complete_profile.html")


from django.shortcuts import get_object_or_404

# def tutor_public_profile(request, user_id):

#     tutor = get_object_or_404(TutorProfile, user__id=user_id)

#     return render(request, "tutor/tutor_public_profile.html", {
#         "tutor": tutor
#     })


import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import io
import base64
from django.shortcuts import render, get_object_or_404
from tutor.models import TutorProfile


def tutor_public_profile(request, user_id):

    tutor = get_object_or_404(TutorProfile, user__id=user_id)

    # ================= GRAPH =================
    labels = ["Rating"]
    values = [tutor.rating]

    plt.figure(figsize=(5,4))
    plt.style.use("dark_background")

    bars = plt.bar(labels, values)

    # Neon cyan bar color
    for bar in bars:
        bar.set_color("#38bdf8")

    plt.title("Overall Tutor Rating", color="white", fontsize=14)
    plt.ylim(0, 5)
    plt.grid(axis="y", alpha=0.2)

    buffer = io.BytesIO()
    plt.savefig(
        buffer,
        format="png",
        bbox_inches="tight",
        facecolor="#020617"
    )
    buffer.seek(0)

    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png).decode("utf-8")

    buffer.close()
    plt.close()

    return render(request, "tutor/tutor_public_profile.html", {
        "tutor": tutor,
        "rating_graph": graph
    })


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# ===============================
# VIEW AVAILABLE SLOTS
# ===============================
@login_required
def tutor_slots(request, tutor_id, skill_name):

    tutor = get_object_or_404(TutorProfile, id=tutor_id)

    # Filter slots by skill
    all_slots = tutor.availabilities.filter(skill_name__iexact=skill_name)

    # Remove already booked slots
    booked_slot_ids = Booking.objects.filter(
        tutor=tutor
    ).values_list("availability_id", flat=True)

    available_slots = all_slots.exclude(id__in=booked_slot_ids)

    return render(request, "tutor/view_slots.html", {
        "tutor": tutor,
        "slots": available_slots,
        "selected_skill": skill_name
    })



# ===============================
# BOOK SLOT
# ===============================
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

@login_required
def book_slot(request, slot_id):

    slot = get_object_or_404(Availability, id=slot_id)

    already_booked = Booking.objects.filter(
        availability=slot
    ).exists()

    if already_booked:
        messages.error(request, "Slot already booked")
        return redirect("tutor:tutor_slots", tutor_id=slot.tutor.id)

    # Create booking
    booking = Booking.objects.create(
        student=request.user,
        tutor=slot.tutor,
        availability=slot
    )

    # Generate unique Jitsi meeting link
    room_name = f"skilllink-{booking.id}-{uuid.uuid4().hex[:6]}"
    meeting_link = f"https://meet.jit.si/{room_name}"

    booking.meeting_link = meeting_link
    booking.save()

    # ===== EMAIL CONTENT =====
    subject = "SkillLink Booking Confirmation 🎉"

    message = f"""
Booking Confirmed!

Skill: {slot.skill_name}

Tutor: {slot.tutor.user.username}
Student: {request.user.username}

Date: {slot.date}
Time: {slot.start_time} - {slot.end_time}

Meeting Link:
{meeting_link}

Thank you for using SkillLink 🚀
"""

    # Send to student
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [request.user.email],
        fail_silently=False,
    )

    # Send to tutor
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [slot.tutor.user.email],
        fail_silently=False,
    )

    messages.success(request, "Booking successful! Confirmation email sent.")

    return redirect("tutor:booking_receipt", booking_id=booking.id)




# ===============================
# BOOKING RECEIPT PAGE
# ===============================
@login_required
def booking_receipt(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        student=request.user
    )

    return render(request, "tutor/booking_receipt.html", {
        "booking": booking
    })
# ===============================
# DOWNLOAD RECEIPT (.txt)
# ===============================
@login_required
def download_receipt(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        student=request.user
    )

    content = f"""
SkillLink Booking Receipt
----------------------------

Tutor: {booking.tutor.user.first_name or booking.tutor.user.username}
Student: {booking.student.username}
Date: {booking.availability.date}
Time: {booking.availability.start_time} - {booking.availability.end_time}

Meeting Link:
{booking.meeting_link}

Booked At:
{booking.booked_at}

Status:
{booking.status}
"""

    response = HttpResponse(content, content_type="text/plain")
    response["Content-Disposition"] = f'attachment; filename="receipt_{booking.id}.txt"'

    return response

@login_required
def edit_slot(request, slot_id):

    slot = get_object_or_404(
        Availability,
        id=slot_id,
        tutor=request.user.tutor_profile
    )

    if request.method == "POST":

        if "delete" in request.POST:
            slot.delete()
            return redirect("tutor:tutor_dashboard")

        # Update slot
        slot.skill_name = request.POST.get("skill_name")
        slot.date = request.POST.get("date")
        slot.start_time = request.POST.get("start_time")
        slot.end_time = request.POST.get("end_time")

        slot.save()

        return redirect("tutor:tutor_dashboard")

    return render(request, "tutor/edit_slot.html", {
        "slot": slot
    })


@login_required
def add_slot(request):

    profile = request.user.tutor_profile

    if request.method == "POST":

        skill_name = request.POST.get("skill_name")
        date = request.POST.get("date")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")

        if skill_name and date and start_time and end_time:
            Availability.objects.create(
                tutor=profile,
                skill_name=skill_name,
                date=date,
                start_time=start_time,
                end_time=end_time
            )

        return redirect("tutor:tutor_dashboard")

    return render(request, "tutor/add_slot.html")

@login_required
def session_history(request):

    profile = request.user.tutor_profile

    completed_sessions = Booking.objects.filter(
        tutor=profile,
        status="completed"
    ).select_related("student", "availability").order_by("-booked_at")

    return render(request, "tutor/session_history.html", {
        "completed_sessions": completed_sessions
    })


from client.models import ClientProfile

@login_required
def company_profile(request, user_id):

    from client.models import ClientProfile
    from django.shortcuts import get_object_or_404

    client_profile = get_object_or_404(
        ClientProfile,
        user__id=user_id
    )

    return render(request, "tutor/company_profile.html", {
        "client_profile": client_profile
    })


# from django.shortcuts import render,redirect

# from numpy import random
# from django.core.mail import send_mail
# import time
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login

# def tutor_login(request):
#     mode = request.GET.get("mode")  # login OR signup
#     if mode=="login":
#         return login_form(request)
#     if mode=="signup":
#         return tutor_register(request)
#     return render(request, "tutor_auth.html", {"mode": mode})

# def login_form(request):

#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         user = authenticate(request, email=email, password=password)

#         if user is None:
#             return render(request, "tutor/login.html", {
#                 "email": email,
#                 "pass_error": "Invalid email or password"
#             })

#         login(request, user)
#         request.session["email"] = email
#         # return redirect("tutor_login")
#         print("login successful!")
#         # return redirect("dashboard")
#     return render(request, "tutor/login.html")

# def tutor_register(request):
#     action = request.POST.get("action")
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         confirm_password = request.POST.get("confirm_password")
#         otp = request.POST.get("otp")

#         cap=0
#         special=['_','@','$']
#         sp=0
#         num=0

#         already_register=User.objects.filter(email=email).exists()

#         if not (email.endswith("@gmail.com") 
#             or email.endswith("@yahoo.com") 
#             or email.endswith("@outlook") 
#             or email.endswith("@aol.com") 
#             or email.endswith("@hotmail.com") 
#             or email.endswith("@zoho.com") 
#             or email.endswith("@icloud.com")):
#             return render(request, "tutor/signup.html", 
#                           {"email_error": "Please enter a valid email provider",
#                            "email": email})
        
#         if already_register:
#             return render(request, "tutor/signup.html", 
#                           {"email_error": "This email is already registered!",
#                            "email": email})

#         # STEP 1 — SEND OTP
#         if action == "send_otp":
#             request.session.pop("otp", None)
#             generated_otp = otp_generation()
#             request.session["otp"] = generated_otp
#             request.session["email"] = email

#             send_mail(
#                 "SkillLink OTP Verification",
#                 f"Your SkillLink OTP is: {generated_otp}",
#                 "skill.link.connects@gmail.com",
#                 [email],
#             )

#             return render(request, "core/signup.html", {
#                 "email": email,
#                 "show_otp": True,
#                 "show_password": False,
#                 "info": "OTP sent successfully"
#             })

#         # STEP 2 — VERIFY OTP
#         if action == "verify_otp":
#             session_otp = request.session.get("otp")

#             if not session_otp or str(otp) != str(session_otp):
#                 return render(request, "tutor/signup.html", {
#                     "email": email,
#                     "show_otp": True,
#                     "show_password": False,
#                     "otp": otp,
#                     "otp_error": "Incorrect OTP"
#                 })

#             return render(request, "tutor/signup.html", {
#                     "email": email,
#                     "show_otp": True,
#                     "show_password": True,
#                     "otp": otp,
#                     "otp_success": "OTP verified successfully"})


#         if action == "create_account":
#             if not password==confirm_password:
#                 return render(request, "tutor/signup.html", 
#                     {"match_error": "Passcodes do not match",
#                     "email": email,
#                     "otp": otp,
#                     "show_otp": True,
#                     "show_password": True,
#                     })

#             if len(password)<8 or len(password)>12:
#                 return render(request, "tutor/signup.html",
#                     {"pass_error": "Passcodes must be between the length of 8 to 12 character",
#                         "email": email,
#                         "otp": otp,
#                         "show_otp": True,
#                         "show_password": True,})
                
#             for i in password:
#                 if i.isupper():
#                     cap+=1
#                 if i in special:
#                     sp+=1
#                 if i.isdigit():
#                     num+=1
#             if cap==0:
#                 return render(request, "tutor/signup.html",
#                     {"pass_error": "Passcodes must contain atleast 1 capital aplhabet",
#                         "email": email,
#                         "otp": otp,
#                         "show_otp": True,
#                         "show_password": True,})
#             if num==0:
#                 return render(request, "tutor/signup.html",
#                     {"pass_error": "Passcodes must contain a number",
#                         "email": email,
#                         "otp": otp,
#                         "show_otp": True,
#                         "show_password": True,})
#             if sp==0:
#                 return render(request, "tutor/signup.html",
#                     {"pass_error": "Passcodes must contain a special character from _, @, $",
#                         "email": email,
#                         "otp": otp,
#                         "show_otp": True,
#                         "show_password": True,})  
            
#             User.objects.create_user(
#                                         username=email,
#                                         email=email,
#                                         password=password
#                                     )


#             # CLEAN SESSION
#             request.session.pop("otp", None)

#             # return render(request, "tutor/signup.html", {
#             #     "success": "Account created successfully!"
#             # })
#             request.session["email"] = email
#             # return redirect("dashboard")
#             return redirect("tutor_login")

#     return render(request, "tutor/signup.html", {
#                         "show_otp": False,
#                         "show_password": False
#                     })


# def otp_generation():
#     x=random.randint(0,10,size=(6,))
#     otp=""
#     for i in x:
#         otp+=str(i)
#     otp=int(otp)
#     return otp
        
# def dashboard(request):

#     email = request.session.get("email")

#     if not email:
#         return redirect("learn_login")

#     return render(request, "core/learn_dashboard.html", {
#     "profile_completed": False
# })

# def profile(request):

#     email = request.session.get("email")

#     if not email:
#         return redirect("learn_login")

#     if request.method == "POST":
#         request.session["profile_completed"] = True
#         return redirect("dashboard")

#     return render(request, "core/student_profile.html")


#Changes

from django.shortcuts import render, redirect, get_object_or_404
from client.models import HiringRequest
from django.contrib.auth.decorators import login_required


from .models import TutorProfile
from client.models import HiringRequest

@login_required
def tutor_notifications(request):

    #profile = TutorProfile.objects.get(user=request.user)
    tutor_profile = request.user.tutor_profile

    requests = HiringRequest.objects.filter(
        tutor=tutor_profile
    ).order_by('-created_at')

    return render(request, 'tutor/notifications.html', {
        'requests': requests
    })

@login_required
def accept_request(request, request_id):

    tutor_profile = request.user.tutor_profile

    hiring_request = get_object_or_404(
        HiringRequest,
        id=request_id,
         tutor=tutor_profile  
    )

    hiring_request.status = 'accepted'
    hiring_request.save()

    return redirect('tutor:tutor_notifications')
@login_required
def reject_request(request, request_id):

    tutor_profile = request.user.tutor_profile
    
    hiring_request = get_object_or_404(
        HiringRequest,
        id=request_id,
        tutor=tutor_profile
    )

    hiring_request.status = 'rejected'
    hiring_request.save()

    return redirect('tutor:tutor_notifications')