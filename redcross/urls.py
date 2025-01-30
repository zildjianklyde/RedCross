from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('django-admin/', admin.site.urls),  # Rename Django's admin
    path('admin/', include('app.urls')),     # Your custom admin URLs
    path('', include('app.urls')),           
]