from django.urls import path
from . import views


urlpatterns = [
    # Public URLs
    path('', views.landing_page, name='landing'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('eligibility/', views.eligibility_check, name='eligibility_check'),
    path('donor-dashboard/', views.donor_dashboard, name='donor_dashboard'),
    path('profile/', views.profile, name='profile'),
 

    # Admin URLs
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/manage-users/', views.manage_users, name='manage_users'),
    path('admin/create-donor/', views.create_donor, name='create_donor'),
    path('admin/edit-user/<int:pk>/', views.edit_user, name='edit_user'),
    path('admin/delete-user/<int:pk>/', views.delete_user, name='delete_user'),
    path('admin/update-donor/<int:id>/', views.update_donor, name='update_donor'),
    path('admin/delete-donor/<int:id>/', views.delete_donor, name='delete_donor'),
    path('admin/edit-user/<int:pk>/', views.edit_user, name='edit_user'),
path('admin/delete-user/<int:pk>/', views.delete_user, name='delete_user'),
]
