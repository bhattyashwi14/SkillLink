from django.contrib import admin
from django.urls import path, include
from tutor import views

from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('tutor',views.tutor_auth,name='tutor'),
    # path("tutor/", views.tutor_login, name="tutor_login"),
    # path('register/', views.tutor_register, name='tutor_register'),
    # path('login/', views.tutor_login, name='tutor_login'),     
    path('tutor/login/', views.tutor_login_form, name='tutor_login'),
    path('tutor/register/', views.tutor_register, name='tutor_register'),
    path("complete-profile/", views.complete_profile, name="complete_profile"),
    path("dashboard/", views.tutor_dashboard, name="tutor_dashboard"),
    path('logout/', LogoutView.as_view(next_page='tutor_login'), name='logout'),

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
    path('slots/<int:tutor_id>/', views.tutor_slots, name='tutor_slots'),
    path('book-slot/<int:slot_id>/', views.book_slot, name='book_slot'),
]

