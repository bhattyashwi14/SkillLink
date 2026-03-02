from django.contrib import admin
from django.urls import path, include
from tutor import views

from django.contrib.auth.views import LogoutView

app_name = "tutor"

# urlpatterns = [
#     path('tutor',views.tutor_auth,name='tutor'),
#     # path("tutor/", views.tutor_login, name="tutor_login"),
#     # path('register/', views.tutor_register, name='tutor_register'),
#     # path('login/', views.tutor_login, name='tutor_login'),     
#     path('tutor/login/', views.tutor_login_form, name='tutor_login'),
#     path('tutor/register/', views.tutor_register, name='tutor_register'),
#     path("complete-profile/", views.complete_profile, name="complete_profile"),
#     path("dashboard/", views.tutor_dashboard, name="tutor_dashboard"),
#     path('logout/', LogoutView.as_view(next_page='tutor_login'), name='logout'),

# urlpatterns = [
#     path('tutor',views.tutor_auth,name='tutor'),
#     # path("tutor/", views.tutor_login, name="tutor_login"),
#     # path('register/', views.tutor_register, name='tutor_register'),
#     # path('login/', views.tutor_login, name='tutor_login'),     
#     path('tutor/login/', views.tutor_login_form, name='tutor_login'),
#     path('tutor/register/', views.tutor_register, name='tutor_register'),
#     path("complete-profile/", views.complete_profile, name="complete_profile"),
#     path("dashboard/", views.tutor_dashboard, name="tutor_dashboard"),
#     path("tutor/profile/<int:user_id>/", views.tutor_public_profile, name="tutor_public_profile"),
# ]


urlpatterns = [
    path('', views.tutor_auth, name='tutor'),
    path('login/', views.tutor_login_form, name='tutor_login'),
    path('register/', views.tutor_register, name='tutor_register'),
    path('complete-profile/', views.complete_profile, name='complete_profile'),
    path('dashboard/', views.tutor_dashboard, name='tutor_dashboard'),

    path('profile/<int:user_id>/', views.tutor_public_profile, name='tutor_public_profile'),


    # ⭐ SLOT SYSTEM
    path("slots/<int:tutor_id>/<str:skill_name>/", views.tutor_slots, name="tutor_slots"),
    path('slot/edit/<int:slot_id>/', views.edit_slot, name='edit_slot'),
    path('slot/add/', views.add_slot, name='add_slot'),
    path("sessions/history/", views.session_history, name="session_history"),
    path('book-slot/<int:slot_id>/', views.book_slot, name='book_slot'),
    path('booking-receipt/<int:booking_id>/', views.booking_receipt, name='booking_receipt'),
    path('download-receipt/<int:booking_id>/', views.download_receipt, name='download_receipt'),
    path('logout/', LogoutView.as_view(next_page='tutor:tutor_login'), name='logout'),
    path(
        'notifications/',
        views.tutor_notifications,
        name='tutor_notifications'
    ),

    path(
        'accept/<int:request_id>/',
        views.accept_request,
        name='accept_request'
    ),

    path(
        'reject/<int:request_id>/',
        views.reject_request,
        name='reject_request'
    ),

    path(
    'company/<int:user_id>/',
    views.company_profile,
    name='company_profile'
    ),

]

