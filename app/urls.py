from django.urls import path
from .import views

urlpatterns = [
    path('', views.indexview.as_view(), name='index'),
    path('list/', views.listview.as_view(), name='list'),
    path('create/', views.createview.as_view(), name='create'),
    path('delete/<int:pk>',views.deleteview.as_view(), name='delete'),
    path('update/<int:pk>',views.updateview.as_view(), name='update'),

]