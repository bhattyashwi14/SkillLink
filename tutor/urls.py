from django.contrib import admin
from django.urls import path, include
from tutor import views
urlpatterns = [
    path('tutor',views.tutor_auth,name='tutor'),
    # path("tutor/", views.tutor_login, name="tutor_login"),
    # path('register/', views.tutor_register, name='tutor_register'),
    # path('login/', views.tutor_login, name='tutor_login'),     
    path('tutor/login/', views.tutor_login_form, name='tutor_login'),
    path('tutor/register/', views.tutor_register, name='tutor_register'),
    path("complete-profile/", views.complete_profile, name="complete_profile"),
    path("dashboard/", views.tutor_dashboard, name="tutor_dashboard"),


]