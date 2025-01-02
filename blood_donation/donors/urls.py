from django.urls import path
from .views import DonorCreateView, DonorListView, DonorDetailView, DonorUpdateView, DonorDeleteView
from django.contrib.auth.views import LoginView, LogoutView  # Correct import for LogoutView
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('', DonorListView.as_view(), name='donor_list'),
    path('add/', DonorCreateView.as_view(), name='donor_add'),
    path('<int:pk>/', DonorDetailView.as_view(), name='donor_detail'),
    path('<int:pk>/edit/', DonorUpdateView.as_view(), name='donor_edit'),
    path('<int:pk>/delete/', DonorDeleteView.as_view(), name='donor_delete'),
    path('', views.landing_page, name='landing_page'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='donors/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='donors/logout.html'), name='logout'),  # Use the built-in LogoutView
]
