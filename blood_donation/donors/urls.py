from django.urls import path
from .views import DonorCreateView, DonorListView, DonorDetailView, DonorUpdateView, DonorDeleteView

urlpatterns = [
    path('', DonorListView.as_view(), name='donor_list'),
    path('add/', DonorCreateView.as_view(), name='donor_add'),
    path('<int:pk>/', DonorDetailView.as_view(), name='donor_detail'),
    path('<int:pk>/edit/', DonorUpdateView.as_view(), name='donor_edit'),
    path('<int:pk>/delete/', DonorDeleteView.as_view(), name='donor_delete'),
]
