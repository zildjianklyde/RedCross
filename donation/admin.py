from django.contrib import admin
from .models import CustomUser, Eligibility, Donation

admin.site.register(CustomUser)
admin.site.register(Eligibility)
admin.site.register(Donation)
