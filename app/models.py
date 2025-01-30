from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Database for general donor information
class Database(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    blood = models.CharField(max_length=100)
    date = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse("list")  # Correct indentation

# Donor model for detailed donor-specific information
class Donor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=3, choices=[
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ])
    last_donation_date = models.DateField(null=True, blank=True)
    is_eligible = models.BooleanField(default=True)

    def update_eligibility(self):
        from datetime import date, timedelta
        if self.last_donation_date:
            self.is_eligible = (date.today() - self.last_donation_date) >= timedelta(days=90)
        else:
            self.is_eligible = True
        self.save()
        
    last_donation_date = models.DateField(null=True, blank=True)
    is_eligible = models.BooleanField(default=True)

    def __str__(self):
        return self.user.get_full_name()  

    def update_eligibility(self):
        from datetime import date, timedelta
        if self.last_donation_date:
            self.is_eligible = (date.today() - self.last_donation_date) >= timedelta(days=90)
        else:
            self.is_eligible = True
        self.save()
