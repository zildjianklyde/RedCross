from django.urls import path
from . import views  # Correct import
from django.urls import reverse_lazy  # Fix import issue

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
    path('admin_dashboard/', views.index, name='index'),
    #path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/manage-users/', views.manage_users, name='manage_users'),
    path('admin/create-donor/', views.create_donor, name='create_donor'),
    #path('admin/edit-user/<int:pk>/', views.edit_user, name='edit_user'),
    #path('admin/delete-user/<int:pk>/', views.delete_donor, name='delete_donor'),
    path('admin/update-donor/<int:id>/', views.update_donor, name='update_donor'),
    path('admin/delete-donor/<int:id>/', views.delete_donor, name='delete_donor'),

    # CRUD Operations (CBVs for admin)
    path('list/', views.listview.as_view(), name='list'),
    path('create/', views.createview.as_view(), name='create'),
    path('delete/<int:pk>/', views.deleteview.as_view(), name='delete'),
    path('update/<int:pk>/', views.updateview.as_view(), name='update'),
]
