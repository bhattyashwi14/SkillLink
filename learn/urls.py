from django.urls import path
from . import views 

urlpatterns = [
    path("login/", views.learn_login, name="learn_login"),
     path("dashboard/", views.dashboard, name="dashboard"),
     path("profile/", views.profile, name="profile"),
     path('skill/<str:skill_name>/', views.skill_tutors, name='skill_tutors'),
     path(
    "upcoming-sessions/",
    views.upcoming_sessions,
    name="upcoming_sessions"
    ),

]
