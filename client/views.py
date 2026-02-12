from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
import random

from .models import ClientProfile
from tutor.models import TutorProfile, Skill, Availability
from django.db.models import Q


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Count
from .mock_data import TUTORS 
from tutor.models import Skill



def client_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authenticate user
        user = authenticate(request, username=email, password=password)

        if user is None:
            return render(
                request,
                "client/login.html",
                {
                    "email": email,
                    "pass_error": "Invalid email or password"
                }
            )

        # Login successful
        login(request, user)
        request.session["email"] = email
        return redirect("client-dashboard")
        # return redirect("complete-profile")

    return render(request, "client/login.html")


def client_signup(request):
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
            return render(request, "client/signup.html", 
                          {"email_error": "Please enter a valid email provider",
                           "email": email})
        
        if already_register:
            return render(request, "client/signup.html", 
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

            return render(request, "client/signup.html", {
                "email": email,
                "show_otp": True,
                "show_password": False,
                "info": "OTP sent successfully"
            })

        # STEP 2 — VERIFY OTP
        if action == "verify_otp":
            session_otp = request.session.get("otp")

            if not session_otp or str(otp) != str(session_otp):
                return render(request, "client/signup.html", {
                    "email": email,
                    "show_otp": True,
                    "show_password": False,
                    "otp": otp,
                    "otp_error": "Incorrect OTP"
                })

            return render(request, "client/signup.html", {
                    "email": email,
                    "show_otp": True,
                    "show_password": True,
                    "otp": otp,
                    "otp_success": "OTP verified successfully"})


        if action == "create_account":
            if not password==confirm_password:
                return render(request, "client/signup.html", 
                    {"match_error": "Passcodes do not match",
                    "email": email,
                    "otp": otp,
                    "show_otp": True,
                    "show_password": True,
                    })

            if len(password)<8 or len(password)>12:
                return render(request, "client/signup.html",
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
                return render(request, "client/signup.html",
                    {"pass_error": "Passcodes must contain atleast 1 capital aplhabet",
                        "email": email,
                        "otp": otp,
                        "show_otp": True,
                        "show_password": True,})
            if num==0:
                return render(request, "client/signup.html",
                    {"pass_error": "Passcodes must contain a number",
                        "email": email,
                        "otp": otp,
                        "show_otp": True,
                        "show_password": True,})
            if sp==0:
                return render(request, "client/signup.html",
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
            return redirect("client-dashboard")


    return render(request, "client/signup.html", {
                        "show_otp": False,
                        "show_password": False
                    })


# def otp_generation():
#     x=random.randint(0,10,size=(6,))
#     otp=""
#     for i in x:
#         otp+=str(i)
#     otp=int(otp)
#     return otp
def otp_generation():
    otp = random.randint(100000, 999999)
    return otp

# def client_login(request):

#     # ---------- GET REQUEST ----------
#     if request.method == "GET":
#         return render(request, "client/login.html")

#     # ---------- POST REQUEST ----------
#     email = request.POST.get("email")
#     otp = request.POST.get("otp")

#     # ---------- STEP 1: SEND OTP ----------
#     if email and not otp:

#         # ✅ check if user exists
#         user = User.objects.filter(email=email).first()
#         if not user:
#             return render(request, "client/login.html", {
#                 "error": "Email not registered. Please sign up first."
#             })

#         generated_otp = random.randint(100000, 999999)

#         request.session["login_otp"] = generated_otp
#         request.session["login_email"] = email

#         send_mail(
#             subject="SkillLink Login OTP",
#             message=f"Your OTP is {generated_otp}",
#             from_email=None,
#             recipient_list=[email],
#             fail_silently=False,)

#         return render(request, "client/login.html", {
#             "otp_sent": "OTP sent successfully. Check your email."
#         })

#     # ---------- STEP 2: VERIFY OTP ----------
#     if otp:

#         session_otp = request.session.get("login_otp")
#         session_email = request.session.get("login_email")

#         if not session_otp or not session_email:
#             return render(request, "client/login.html", {
#                 "error": "Session expired. Please try again."
#             })

#         if str(otp) != str(session_otp):
#             return render(request, "client/login.html", {
#                 "error": "Invalid OTP"
#             })

#         # ✅ safe user fetch
#         user = User.objects.filter(email=session_email).first()
#         if not user:
#             return render(request, "client/login.html", {
#                 "error": "User not found. Please sign up."
#             })

#         # ✅ THIS logs the user in
#         login(request, user)

#         # cleanup session
#         request.session.pop("login_otp", None)
#         request.session.pop("login_email", None)

#         return redirect("client-dashboard")

#     # ---------- FALLBACK ----------
#     return render(request, "client/login.html")


#Yashwi UI Ux Changes
# def client_login(request):

#     if request.method == "GET":
#         return render(request, "client/login.html")

#     email = request.POST.get("email")
#     password = request.POST.get("password")

#     # check user exists
#     user_obj = User.objects.filter(email=email).first()

#     if not user_obj:
#         return render(request, "client/login.html", {
#             "email_error": "Email not registered."
#         })

#     # authenticate expects USERNAME
#     user = authenticate(
#         request,
#         username=user_obj.username,
#         password=password
#     )

#     if user is None:
#         return render(request, "client/login.html", {
#             "pass_error": "Invalid password",
#             "email": email
#         })

#     login(request, user)

#     # ⭐ REDIRECT AFTER LOGIN
#     return redirect("complete_profile")



# import random
# from django.conf import settings
# from django.core.mail import send_mail

# def client_signup(request):

#     if request.method == "POST":

#         action = request.POST.get("action")

#         # SEND OTP
#         if action == "send_otp":
#             email = request.POST.get("email")
#             if not email:
#                 return redirect("client-signup") 

#             otp = str(random.randint(100000, 999999))

#             request.session["signup_otp"] = otp
#             request.session["signup_email"] = email

            
#             send_mail(
#     subject="SkillLink OTP",
#     message=f"Your OTP is {otp}",
#     from_email=settings.EMAIL_HOST_USER,
#     recipient_list=[email],
#     fail_silently=False,)

            

#             return render(request, "client/signup.html", {
#                 "show_otp": True,
#                 "email": email
#             })


#         # VERIFY OTP
#         elif action == "verify_otp":

#             entered_otp = request.POST.get("otp")
#             session_otp = request.session.get("signup_otp")

#             if entered_otp == session_otp:
#                 return render(request, "client/signup.html", {
#                     "show_password": True
#                 })
#             else:
#                 return render(request, "client/signup.html", {
#                     "show_otp": True,
#                     "otp_error": "Invalid OTP"
#                 })


#         # CREATE ACCOUNT
#         elif action == "create_account":

#             email = request.session.get("signup_email")
#             if User.objects.filter(email=email).exists(): #
#                 return render(request, "client/signup.html", {
#         "show_password": True,
#         "match_error": "Account already exists. Please login."
#     })

#             password = request.POST.get("password")
#             confirm = request.POST.get("confirm_password")
           

#             if password != confirm:
#                 return render(request, "client/signup.html", {
#                     "show_password": True,
#                     "match_error": "Passwords do not match"
#                 })

#             user = User.objects.create_user(
#                 username=email,
#                 email=email,
#                 password=password
#             )

#             ClientProfile.objects.create(user=user)

#             request.session.pop("signup_email", None)
#             request.session.pop("signup_otp", None)


#             return redirect("client-login")

#     return render(request, "client/signup.html")




# def generate_otp():
#     return str(random.randint(100000, 999999))


# def login_send_otp(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         user = authenticate(username=email, password=password)

#         if user is None:
#             return render(request, "core/index.html", {
#                 "error": "Invalid email or password"
#             })

#         otp = generate_otp()

#         EmailOTP.objects.create(
#             user=user,
#             otp=otp
#         )

#         send_mail(
#             "SkillLink Login OTP",
#             f"Your OTP is {otp}. Valid for 5 minutes.",
#             "skilllink.auth@gmail.com",
#             [email],
#             fail_silently=False
#         )

#         return render(request, "core/index.html", {
#             "otp_sent": True,
#             "email": email
#         })
# def verify_login_otp(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         otp_entered = request.POST.get("otp")

#         user = User.objects.get(email=email)

#         otp_obj = EmailOTP.objects.filter(
#             user=user,
#             otp=otp_entered,
#             is_verified=False
#         ).last()

#         if otp_obj:
#             otp_obj.is_verified = True
#             otp_obj.save()
#             login(request, user)
#             return redirect("dashboard")

#         return render(request, "core/index.html", {
#             "error": "Invalid OTP",
#             "otp_sent": True,
#             "email": email
#         })
import random

# def send_otp(email):
#     otp = random.randint(100000, 999999)
#     # store otp in session or DB
#     return otp


from django.contrib.auth.decorators import login_required
@login_required(login_url="client-login")
def client_dashboard(request):

    client_profile, created = ClientProfile.objects.get_or_create(
    user=request.user
    )

    # ⭐ STOP LOOP HERE
    if not client_profile.is_profile_complete:
        return redirect("complete-profile")


    # ---------- SEARCH ----------
    search_query = request.GET.get('q', '')
    search_by = request.GET.get('search_by') or 'Skill'.lower()
    if TutorProfile:
        tutors = TutorProfile.objects.all()
    else:
        tutors = TUTORS   # fake data


    # tutors = TutorProfile.objects.all()

    if search_query:
        if search_by == 'name':
            tutors = tutors.filter(
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query) |
                Q(user__email__icontains=search_query)
            )

        elif search_by == 'skill':
            tutors = tutors.filter(
                skills__name__icontains=search_query
            )


    # ---------- SKILL CARDS ----------
#     skills = (
#         TutorProfile.objects
#         .values('skills')
#         .annotate(total=Count('id'))
#         .order_by('-total')
#     )

     # ---------- STATS ----------
#     total_jobs = JobPost.objects.filter(client=client_profile).count()

#     total_applications = JobApplication.objects.filter(
#         job__client=client_profile
#     ).count()


#         # Fake Data
#     skills = [
#     {"name": "Python", "total": 12},
#     {"name": "UI/UX", "total": 7},
#     {"name": "Machine Learning", "total": 5},
#     {"name": "Java", "total": 9},
# ]
    # ---------- SKILL SOURCE SWITCH ----------

    USE_FAKE_DATA = False  # ⭐ CHANGE THIS TO FALSE WHEN TUTOR APP ARRIVES
    if USE_FAKE_DATA:
        skills = [
        {"skills": "Python", "total": 12},
        {"skills": "UI/UX", "total": 7},
        {"skills": "Machine Learning", "total": 5},
        {"skills": "Java", "total": 9},
        {"skills": "Cyber Security", "total": 4},
        {"skills": "Data Science", "total": 6},
    ]
        # 🔥 SEARCH ON FAKE DATA
        if search_query and search_by == "skill":
            skills = [
            skill for skill in skills
            if search_query.lower() in skill["skills"].lower()
        ]
            
    else:
        from tutor.models import Skill

        skills = (
            Skill.objects
            .annotate(total=Count("tutorprofile", distinct=True))
            .filter(total__gt=0)
        )

    skills = [
    {"name": skill.name, "total": skill.total}
    for skill in skills
    ]

    # ---------- CONTEXT ----------
    context = {
        'client': client_profile,
        # 'total_jobs': total_jobs,
        # 'total_applications': total_applications,
        'search_query': search_query,
        'search_by': search_by,
        'tutors': tutors,     # used for search results
        'skills': skills      # used for dashboard cards
    }


    return render(request, 'client/dashboard.html', context)

    
    # try:
    #     client_profile = ClientProfile.objects.get(user=request.user)
    #     # if not client_profile.is_profile_complete:
    #     #     return redirect("complete-profile")
    #     if not client_profile.is_profile_complete:
    #         return redirect("complete-profile")

    # except ClientProfile.DoesNotExist:
        # return redirect('client-login')

    
from django.contrib.auth import logout
from django.shortcuts import redirect

def client_logout(request):
    logout(request)
    return redirect("client-login")

from django.contrib.auth.decorators import login_required


# @login_required(login_url="client-login")
# def complete_client_profile(request):
#     client_profile, created = ClientProfile.objects.get_or_create(
#     user=request.user
# )

#     if request.method == "POST":

#         client_profile.company_name = request.POST.get("company_name")
#         client_profile.location = request.POST.get("location")
#         client_profile.bio = request.POST.get("bio")
#         client_profile.linkedin = request.POST.get("linkedin")

#     if request.FILES.get("proof"):
#         client_profile.work_proof = request.FILES.get("proof")


# # ✅ SMART CHECK (Do NOT include proof)
#     if (
#         client_profile.company_name and
#         client_profile.location and
#         client_profile.bio
#     ):
#         client_profile.is_profile_complete = True
#     else:
#         client_profile.is_profile_complete = False


#     client_profile.save()
#     return redirect("client-dashboard")
#     return render(request, "client/complete_profile.html", {
#         "client": client_profile
#     })
@login_required(login_url="client-login")
def complete_client_profile(request):

    client_profile, _ = ClientProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        client_profile.company_name = request.POST.get("company_name")
        client_profile.location = request.POST.get("location")
        client_profile.bio = request.POST.get("bio")
        client_profile.linkedin = request.POST.get("linkedin")

        if request.FILES.get("proof"):
            client_profile.work_proof = request.FILES.get("proof")

        # SMART CHECK
        if (
            client_profile.company_name and
            client_profile.location and
            client_profile.bio
        ):
            client_profile.is_profile_complete = True
        else:
            client_profile.is_profile_complete = False

        client_profile.save()

        # ✅ ONLY redirect AFTER saving POST
        return redirect("client-dashboard")


    # ✅ GET request → show page
    return render(request, "client/complete_profile.html", {
        "client": client_profile
    })

    # profile = ClientProfile.objects.get(user=request.user)


    # if request.method == "POST":

    #     profile.company_name = request.POST.get("company_name")

    #     if not profile.company_name:
    #         return redirect("complete-client-profile")~

    #     profile.location = request.POST.get("location")
    #     profile.bio = request.POST.get("bio")
    #     profile.linkedin = request.POST.get("linkedin")

    #     if request.FILES.get("proof"):
    #         profile.proof = request.FILES.get("proof")

    #     profile.save()

    #     return redirect("client-dashboard")

    # return render(request, "client/complete_profile.html")





# for fake data

def skill_detail(request, skill_name):

    USE_FAKE_DATA = False
    search_query = request.GET.get("search", "")

    if USE_FAKE_DATA:

        interns = [
            {"id":1,"name": "Aarav Sharma", "skill": "python", "rating": 4.9},
            {"id":2,"name": "Riya Patel", "skill": "python", "rating": 4.7},
            {"id":3,"name": "Kabir Mehta", "skill": "java", "rating": 4.5},
            {"id":4,"name": "Sneha Iyer", "skill": "Uiux", "rating": 4.8},
            {"id":5,"name": "Kriti", "skill": "Uiux", "rating": 4.7},
            {"id":6,"name": "Abhishek", "skill": "Uiux", "rating": 4.3},
            {"id":7,"name": "Rohit", "skill": "Uiux", "rating": 4.2},
            {"id":8,"name": "Arunita", "skill": "Uiux", "rating": 4.9},
            {"id":9,"name": "Lakshmi", "skill": "Uiux", "rating": 5},
            {"id":10,"name": "Jethalal", "skill": "Uiux", "rating": 4.3},
            {"id":11,"name": "Tapu", "skill": "Uiux", "rating": 4.1},
        ]

        interns = [
            i for i in TUTORS
            if i["skill"].lower() == skill_name.lower()
        ]

        if search_query:
            interns = [
                i for i in TUTORS
                if search_query.lower() in i["name"].lower()
            ]

        interns.sort(key=lambda x: x["rating"], reverse=True)

    else:

        interns = TutorProfile.objects.filter(
            skills__name__icontains=skill_name
        ).distinct()


        if search_query:
            interns = interns.filter(
                user__first_name__icontains=search_query
            )

        interns = interns.order_by("-rating")
    no_results = False

    if search_query and len(interns) == 0:
        no_results = True


    context = {
        "skill_name": skill_name.title(),
        "interns": interns,
        "search_query": search_query,
        "total_candidates": len(interns) if USE_FAKE_DATA else interns.count(),
        "no_results": no_results
    }

    return render(request, "client/skill_detail.html", context)


def tutor_profile(request, id):

    USE_FAKE_DATA = False

    if USE_FAKE_DATA:

        tutor = next(
            (t for t in TUTORS if t["id"] == id),
            None
        )

    else:
        tutor_obj = TutorProfile.objects.select_related("user").get(id=id)

        availability = tutor_obj.availabilities.all()
        
        tutor = {
                "id": tutor_obj.id,
                "name": (
                    tutor_obj.user.get_full_name()
                    or tutor_obj.user.first_name
                    or tutor_obj.user.username
                ),
                "bio": tutor_obj.bio or "",
                "skills": tutor_obj.skills.all(),
                "rating": tutor_obj.rating or 0,
                "linkedin": tutor_obj.linkedin or "",
                "github": tutor_obj.github or "",
                "availability": availability,
            }
        return render(request, "client/tutor_profile.html", {
                "tutor": tutor_obj,
                "availability": availability
            })
    return render(request,"client/tutor_profile.html", {
        "tutor": tutor
    })



from .models import HiringRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


@login_required
def hire_tutor(request, tutor_id):
    
    USE_FAKE_DATA=False
    if USE_FAKE_DATA:
        tutor = next((t for t in TUTORS if t["id"] == tutor_id), None)

    else:
        tutor = get_object_or_404(TutorProfile, id=tutor_id)

    if request.method == "POST":

        skill = request.POST.get("skill")
        budget = request.POST.get("budget")
        duration = request.POST.get("duration")
        mode = request.POST.get("mode")
        description = request.POST.get("description")

        HiringRequest.objects.create(
            client=request.user,
            tutor=tutor,
            skill=skill,
            budget=budget,
            duration=duration,
            mode=mode,
            description=description,
        )

        return redirect("request_success")

    return render(request, "client/hire_tutor.html", {
        "tutor": tutor
    })
def request_success(request):
    return render(request, "client/request_success.html")


@login_required
def my_requests(request):
    requests = HiringRequest.objects.filter(client=request.user).order_by('-created_at')

    return render(request, "client/my_requests.html", {
        "requests": requests
    })
