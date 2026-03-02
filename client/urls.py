from django.urls import path
from . import views
from .views import client_login,client_signup,client_dashboard,client_logout

urlpatterns = [
    
    path('login/', views.client_login, name='client-login'),
    path('signup/', views.client_signup, name='client-signup'),
    # path("login/send-otp/", login_send_otp, name="login_send_otp"),
    # path("login/verify-otp/", verify_login_otp, name="verify_login_otp"),
    path('dashboard/', client_dashboard, name='client-dashboard'),
    path("logout/", views.client_logout, name="client-logout"),
    # path(
    #     "complete-profile/",
    #     views.complete_client_profile,
    #     name="complete-client-profile"
    # ),
    path(
    "complete-profile/",
    views.complete_client_profile,
    name="complete-profile"
),
# path('tutor/<int:tutor_id>/', views.tutor_profile, name='tutor_profile')
path('tutor/<int:id>/', views.tutor_profile, name='tutor_profile'),
path('hire/<int:tutor_id>/', views.hire_tutor, name='hire_tutor'),
path("request-success/", views.request_success, name="request_success"),
path("my-requests/", views.my_requests, name="my_requests"),
path("skills/<int:skill_id>/", views.skill_detail, name="skill-detail"),
# path('tutor/<int:tutor_id>/', views.tutor_profile, name='tutor_profile')
path('tutor/<int:id>/', views.tutor_profile, name='tutor_profile'),
path('hire/<int:tutor_id>/', views.hire_tutor, name='hire_tutor'),
path("request-success/", views.request_success, name="request_success"),
path("my-requests/", views.my_requests, name="my_requests"),


]



