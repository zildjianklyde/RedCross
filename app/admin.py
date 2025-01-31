from django.contrib import admin
from .models import Donor

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('user', 'eligibility_status', 'last_donation_date')
    readonly_fields = ('eligibility_data',)
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'blood_type')
        }),
        ('Eligibility', {
            'fields': ('eligibility_status', 'eligibility_data')
        }),
        ('Donation History', {
            'fields': ('last_donation_date', 'is_eligible')
        }),
    )