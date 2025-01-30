from django.urls import path
from .import views

urlpatterns = [
   path('', views.landing_page, name='landing'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),  
    path('logout/', views.logout_view, name='logout'),
    path('eligibility/', views.eligibility_check, name='eligibility_check'),
    path('donor_dashboard/', views.donor_dashboard, name='donor_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/manage-users/', views.manage_users, name='manage_users'),
    path('admin/edit-user/<int:pk>/', views.edit_user, name='edit_user'),
    path('admin/delete-user/<int:pk>/', views.delete_user, name='delete_user'),
    path('profile/', views.profile, name='profile'),

    path('index/', views.IndexView.as_view(), name='index'),
    path('list/', views.ListView.as_view(), name='list'),
    path('create/', views.CreateView.as_view(), name='create'),
    path('delete/<int:pk>/', views.DeleteView.as_view(), name='delete'),
    path('update/<int:pk>/', views.UpdateView.as_view(), name='update'),
]