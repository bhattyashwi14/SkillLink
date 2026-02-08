from django.urls import path
from . import views 

urlpatterns = [
    path("login/", views.learn_login, name="learn_login"),
     path("dashboard/", views.dashboard, name="dashboard"),
     path("profile/", views.profile, name="profile"),
]
