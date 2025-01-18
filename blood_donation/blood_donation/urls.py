from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # For the admin interface
    path('', include('donors.urls')),  # Include the URLs from your app
]
