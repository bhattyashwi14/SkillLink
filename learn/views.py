from django.shortcuts import render,redirect
from numpy import random
from django.core.mail import send_mail
import time
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from core.models import StudentProfile
from tutor.models import Skill, TutorProfile, Booking


from tutor.models import TutorProfile, Skill 
from django.shortcuts import get_object_or_404

def learn_login(request):
    mode = request.GET.get("mode")  # login OR signup
    if mode=="login":
        return login_form(request)
    if mode=="signup":
        return signup(request)
    return render(request, "core/entry.html", {"mode": mode})

def login_form(request):

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is None:
            return render(request, "core/login.html", {
                "email": email,
                "pass_error": "Invalid email or password"
            })

        login(request, user)
        request.session["email"] = email
        return redirect("dashboard")
    return render(request, "core/login.html")

def signup(request):
    action = request.POST.get("action")
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        otp = request.POST.get("otp")

        cap=0
        special=['_','@','$']
        sp=0
        num=0

        already_register=User.objects.filter(email=email).exists()

        if not (email.endswith("@gmail.com") 
            or email.endswith("@yahoo.com") 
            or email.endswith("@outlook") 
            or email.endswith("@aol.com") 
            or email.endswith("@hotmail.com") 
            or email.endswith("@zoho.com") 
            or email.endswith("@icloud.com")):
            return render(request, "core/signup.html", 
                          {"email_error": "Please enter a valid email provider",
                           "email": email})
        
        if already_register:
            return render(request, "core/signup.html", 
                          {"email_error": "This email is already registered!",
                           "email": email})

        # STEP 1 — SEND OTP
        if action == "send_otp":
            request.session.pop("otp", None)
            generated_otp = otp_generation()
            request.session["otp"] = generated_otp
            request.session["email"] = email

            send_mail(
                "SkillLink OTP Verification",
                f"Your SkillLink OTP is: {generated_otp}",
                "skill.link.connects@gmail.com",
                [email],
            )

            return render(request, "core/signup.html", {
                "email": email,
                "show_otp": True,
                "show_password": False,
                "info": "OTP sent successfully"
            })

        # STEP 2 — VERIFY OTP
        if action == "verify_otp":
            session_otp = request.session.get("otp")

            if not session_otp or str(otp) != str(session_otp):
                return render(request, "core/signup.html", {
                    "email": email,
                    "show_otp": True,
                    "show_password": False,
                    "otp": otp,
                    "otp_error": "Incorrect OTP"
                })

            return render(request, "core/signup.html", {
                    "email": email,
                    "show_otp": True,
                    "show_password": True,
                    "otp": otp,
                    "otp_success": "OTP verified successfully"})


        if action == "create_account":
            if not password==confirm_password:
                return render(request, "core/signup.html", 
                    {"match_error": "Passcodes do not match",
                    "email": email,
                    "otp": otp,
                    "show_otp": True,
                    "show_password": True,
                    })

            if len(password)<8 or len(password)>12:
                return render(request, "core/signup.html",
                    {"pass_error": "Passcodes must be between the length of 8 to 12 character",
                        "email": email,
                        "otp": otp,
                        "show_otp": True,
                        "show_password": True,})
                
            for i in password:
                if i.isupper():
                    cap+=1
                if i in special:
                    sp+=1
                if i.isdigit():
                    num+=1
            if cap==0:
                return render(request, "core/signup.html",
                    {"pass_error": "Passcodes must contain atleast 1 capital aplhabet",
                        "email": email,
                        "otp": otp,
                        "show_otp": True,
                        "show_password": True,})
            if num==0:
                return render(request, "core/signup.html",
                    {"pass_error": "Passcodes must contain a number",
                        "email": email,
                        "otp": otp,
                        "show_otp": True,
                        "show_password": True,})
            if sp==0:
                return render(request, "core/signup.html",
                    {"pass_error": "Passcodes must contain a special character from _, @, $",
                        "email": email,
                        "otp": otp,
                        "show_otp": True,
                        "show_password": True,})  
            
            User.objects.create_user(
                                        username=email,
                                        email=email,
                                        password=password
                                    )


            # CLEAN SESSION
            request.session.pop("otp", None)

            # return render(request, "core/signup.html", {
            #     "success": "Account created successfully!"
            # })
            request.session["email"] = email
            request.session["profile_completed"] = False
            return redirect("profile")



    return render(request, "core/signup.html", {
                        "show_otp": False,
                        "show_password": False
                    })


def otp_generation():
    x=random.randint(0,10,size=(6,))
    otp=""
    for i in x:
        otp+=str(i)
    otp=int(otp)
    return otp


def dashboard(request):

    email = request.session.get("email")

    if not email:
        return redirect("learn_login")

    # Safe user fetch
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return redirect("learn_login")

    # Ensure student profile exists
    profile, created = StudentProfile.objects.get_or_create(user=user)

    available_skills = Skill.objects.all()
    print(f"DEBUG: Number of skills found: {available_skills.count()}")
    for s in available_skills:
        print(f"DEBUG: Skill Name: {s.name}")
    # Force profile completion for new users
    if not profile.profile_completed:
        return redirect("profile")
    
    # available_skills = Skill.objects.filter(
    #     tutorprofile__is_approved=True
    # ).distinct()
    available_teaching_skills = TutorProfile.objects.filter(
        is_approved=True
    ).exclude(
        teaching_skills__isnull=True
    ).exclude(
        teaching_skills=""
    ).values_list('teaching_skills', flat=True).distinct()
    # Avatar letter logic
    # Force profile completion
    if not profile.profile_completed:
        return redirect("profile")

    # Avatar logic
    avatar_letter = "S"
    if profile.full_name:
        avatar_letter = profile.full_name[0].upper()


    
    # available_skills = Skill.objects.all() 

    # Keep your debug prints to be sure
    print(f"DEBUG: Number of skills found: {available_skills.count()}")

    
    # Profile completion percentage

    # Profile completion %
    completion = 0
    if profile.full_name:
        completion += 20
    if profile.semester:
        completion += 20
    if profile.department:
        completion += 20
    if profile.skills:
        completion += 20
    if profile.linkedin:
        completion += 10
    if profile.github:
        completion += 10

    # ===============================
    # ⭐ SKILL → TUTOR COUNT LOGIC
    # ===============================

    skills_data = []

    # ⭐ BOOKING COUNT MUST BE OUTSIDE LOOP
    upcoming_sessions_count = Booking.objects.filter(
    student=user
        ).count()


    skills = Skill.objects.all()

    for skill in skills:

        approved_tutors = TutorProfile.objects.filter(
            skills__id=skill.id,
            is_approved=True
        ).distinct()

        tutor_count = approved_tutors.count()

        if tutor_count > 0:
            skills_data.append({
                "name": skill.name,
                "count": tutor_count
            })




    return render(request, "core/learner_dashboard.html", {
    "profile_completed": profile.profile_completed,
    "profile": profile,
    "avatar_letter": avatar_letter,
    "profile_completion": completion,
    "skills_data": skills_data,
    "upcoming_sessions_count": upcoming_sessions_count,
        })





def profile(request):

    email = request.session.get("email")

    if not email:
        return redirect("learn_login")

    user = User.objects.get(email=email)

    # Ensure profile exists
    profile, created = StudentProfile.objects.get_or_create(user=user)

    if request.method == "POST":

        profile.full_name = request.POST.get("full_name")
        profile.semester = request.POST.get("semester")
        profile.department = request.POST.get("department")
        profile.skills = request.POST.get("skills")
        profile.linkedin = request.POST.get("linkedin")
        profile.github = request.POST.get("github")

        profile.profile_completed = True
        profile.save()

        return redirect("dashboard")

    return render(request, "core/learner_profile.html", {
        "profile": profile
    })

def skill_tutors(request, skill_name):

    skill = Skill.objects.get(name=skill_name)

    tutors = TutorProfile.objects.filter(
        skills=skill,
        is_approved=True
    )

    return render(request, "core/skill_tutors.html", {
        "skill": skill,
        "tutors": tutors
    })



from tutor.models import Booking
from django.contrib.auth.decorators import login_required


@login_required
def upcoming_sessions(request):

    email = request.session.get("email")

    if not email:
        return redirect("learn_login")

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return redirect("learn_login")

    bookings = Booking.objects.filter(
        student=user,
        status="booked"
    ).select_related("tutor", "availability")

    return render(request, "core/upcoming_sessions.html", {
        "bookings": bookings
    })





