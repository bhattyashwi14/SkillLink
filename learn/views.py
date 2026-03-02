from django.shortcuts import render,redirect
from numpy import random
from django.core.mail import send_mail
import time
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from core.models import StudentProfile
from tutor.models import Skill, TutorProfile, Booking
from tutor.models import Review, TutorProfile
from django.db.models import Avg


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

            if User.objects.filter(username=email).exists():
                return render(request, "core/signup.html", {
                "email_error": "This account already exists. Please login.",
                "email": email,
            })

            if not password == confirm_password:
                return render(request, "core/signup.html", {
                    "match_error": "Passcodes do not match",
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
            
            user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        # ⭐ VERY IMPORTANT — LOGIN USER HERE
        login(request, user)

        # CLEAN SESSION
        request.session.pop("otp", None)

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


from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):

    if not request.user.is_authenticated:
        return redirect("learn_login")

    user = request.user


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

    # ⭐ BOOKING COUNT
    upcoming_sessions_count = Booking.objects.filter(
        student=user,
        status="booked"
    ).count()

    # ⭐ BUILD SKILLS FROM TEACHING_SKILLS TEXT
    skills_map = {}

    approved_tutors = TutorProfile.objects.filter(
    is_approved=True,
    teaching_skills__isnull=False
        ).exclude(teaching_skills="")

    for tutor in approved_tutors:

        raw_skills = tutor.teaching_skills.split(",")

        for skill in raw_skills:

            clean_skill = skill.strip().upper()

            if not clean_skill:
                continue

            skills_map[clean_skill] = skills_map.get(clean_skill, 0) + 1


    # convert to template format
    skills_data = [
        {"name": skill, "count": count}
        for skill, count in skills_map.items()
    ]


    # ===============================
    # COMPLETED SESSIONS → SKILLS LEARNED
    # ===============================

    completed_bookings = Booking.objects.filter(
        student=user,
        status="completed"
    ).select_related("availability")

    learned_skills = list(
        set(
            booking.availability.skill_name
            for booking in completed_bookings
        )
    )

    return render(request, "core/learner_dashboard.html", {
    "profile_completed": profile.profile_completed,
    "profile": profile,
    "avatar_letter": avatar_letter,
    "profile_completion": completion,
    "skills_data": skills_data,
    "upcoming_sessions_count": upcoming_sessions_count,
    "learned_skills": learned_skills, })


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

    normalized_skill = skill_name.strip().upper()

    tutors = TutorProfile.objects.filter(
        is_approved=True
    )

    filtered_tutors = []
    added_ids = set()


    for tutor in tutors:

        if tutor.teaching_skills:

            tutor_skills = [
                s.strip().upper()
                for s in tutor.teaching_skills.split(",")
            ]

            if normalized_skill in tutor_skills and tutor.id not in added_ids:
                filtered_tutors.append(tutor)
                added_ids.add(tutor.id)


    return render(request, "core/skill_tutors.html", {
        "skill_name": skill_name,
        "tutors": filtered_tutors
    })



from tutor.models import Booking
from django.contrib.auth.decorators import login_required


@login_required
def upcoming_sessions(request):

    if not request.user.is_authenticated:
        return redirect("learn_login")

    user = request.user

    bookings = Booking.objects.filter(
        student=user,
        status="booked"
    ).select_related("tutor", "availability")

    return render(request, "core/upcoming_sessions.html", {
        "bookings": bookings
    })
from tutor.models import Review
from django.db.models import Avg

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from tutor.models import Booking, Review, TutorProfile

from django.shortcuts import get_object_or_404, redirect
from tutor.models import Booking
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404
from tutor.models import Booking

@login_required
def mark_completed(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        student=request.user,
        status="booked"
    )

    return redirect("add_review", booking_id=booking.id)


@login_required
def add_review(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        student=request.user,
        status="booked"
    )

    # Prevent duplicate review
    if hasattr(booking, "review"):
        return redirect("dashboard")

    if request.method == "POST":

        rating = int(request.POST.get("rating"))
        review_text = request.POST.get("review_text")

        # Create Review
        Review.objects.create(
            booking=booking,
            student=request.user,
            tutor=booking.tutor,
            rating=rating,
            review_text=review_text
        )

        # ⭐ NOW mark as completed
        booking.status = "completed"
        booking.save()

        tutor = booking.tutor
        tutor.total_students += 1

        avg_rating = tutor.reviews_received.aggregate(
            Avg("rating")
        )["rating__avg"]

        tutor.rating = round(avg_rating, 2)
        tutor.save()

        return redirect("dashboard")

    return render(request, "core/add_review.html", {
        "booking": booking
    })


@login_required
def learned_skills(request):

    bookings = Booking.objects.filter(
        student=request.user,
        status="completed"
    ).select_related("tutor", "availability")

    return render(request, "core/learned_skills.html", {
        "bookings": bookings
    })



from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from tutor.models import Booking

from core.models import StudentProfile

def skills_data_builder():

    skills_map = {}

    approved_tutors = TutorProfile.objects.filter(
        is_approved=True,
        teaching_skills__isnull=False
    ).exclude(teaching_skills="")

    for tutor in approved_tutors:
        raw_skills = tutor.teaching_skills.split(",")

        for skill in raw_skills:
            clean_skill = skill.strip().upper()

            if clean_skill:
                skills_map[clean_skill] = skills_map.get(clean_skill, 0) + 1

    return list(skills_map.keys())

@login_required
def chatbot_response(request):

    actions = []

    message = request.GET.get("message", "").lower()
    last_topic = request.session.get("chat_last_topic")
    user = request.user

    profile = StudentProfile.objects.get(user=user)

    # 🔥 Recalculate completion dynamically
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

    upcoming_sessions = Booking.objects.filter(
        student=user,
        status="booked"
    ).count()

    learned_sessions = Booking.objects.filter(
        student=user,
        status="completed"
    ).count()

    # 🔥 RECOMMENDED SKILLS (Not Yet Learned)
    completed_skills = set(
        Booking.objects.filter(
            student=user,
            status="completed"
        ).values_list("availability__skill_name", flat=True)
    )

    recommended_skills = []

    for skill in skills_data_builder():
        if skill not in completed_skills:
            recommended_skills.append(skill)

    recommended_skills = recommended_skills[:3]  # top 3 only

    # 🔥 SMART DECISION LAYER FIRST
    if message in ["hi", "hello", "hey"]:

        request.session["chat_last_topic"] = None

        if completion < 100:
            response = f"Your profile is {completion}% complete."
            actions = [
                {"label": "Complete Profile", "url": "/learn/profile/"}
            ]

        elif upcoming_sessions == 0:
            response = "You don’t have any upcoming sessions."
            actions = [
                {"label": "Explore Skills", "url": "/learn/dashboard/"}
            ]

        else:
            response = f"You have {upcoming_sessions} upcoming sessions."
            actions = [
                {"label": "View Sessions", "url": "/learn/upcoming-sessions/"}
            ]


    elif "profile" in message:
        request.session["chat_last_topic"] = "profile"
        response = f"Your profile is {completion}% complete."

    elif "session" in message:
        request.session["chat_last_topic"] = "sessions"
        response = f"You have {upcoming_sessions} upcoming sessions."

    elif "skill" in message:
        request.session["chat_last_topic"] = "skills"
        response = f"You have completed {learned_sessions} sessions so far."

    elif "start" in message or "begin" in message:
        if upcoming_sessions == 0:
            response = "You haven't booked any session yet. Try exploring skills!"
        else:
            response = "You already have sessions booked. Keep learning 🚀"
    
    elif (
            "recommend" in message
            or "suggest" in message
            or "what should i learn" in message
            or "what to learn" in message
            or "next skill" in message
        ):
        request.session["chat_last_topic"] = "recommend"

        if recommended_skills:
            response = "Here are some skills you may like:"
            actions = [
                {
                    "label": skill.title(),
                    "url": f"/learn/skill/{skill}/"
                }
                for skill in recommended_skills
            ]
        else:
            response = "You’ve explored all available skills! 🔥"

    elif any(word in message for word in ["how much", "how many", "status", "progress"]):

        if last_topic == "profile":
            response = f"Your profile is {completion}% complete."

        elif last_topic == "sessions":
            response = f"You have {upcoming_sessions} upcoming sessions."

        elif last_topic == "skills":
            response = f"You have completed {learned_sessions} sessions so far."

        else:
            # Intelligent default
            response = f"You have {upcoming_sessions} upcoming sessions and your profile is {completion}% complete."

    else:
        response = "Try asking about your profile, sessions or skills."
    
    return JsonResponse({
    "reply": response,
    "actions": actions
    })


