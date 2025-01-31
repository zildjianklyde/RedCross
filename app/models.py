from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from django.urls import reverse_lazy

class Database(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    contact = models.CharField(max_length=100)
    blood = models.CharField(max_length=100)
    date = models.DateField()

    def get_absolute_url(self):
        return reverse_lazy("list")

class Donor(models.Model):
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES)
    last_donation_date = models.DateField(null=True, blank=True)
    is_eligible = models.BooleanField(default=True)
    eligibility_data = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.blood_type})"
     
    def save(self, *args, **kwargs):
        """Set eligibility before saving to avoid infinite recursion."""
        if not self.pk:  # Avoid recursion loop on save()
            self.is_eligible = self.eligibility_status  
        super().save(*args, **kwargs)

    @property
    def eligibility_status(self):
        """Check if donor is eligible based on last donation date."""
        if self.last_donation_date:
            return (timezone.now().date() - self.last_donation_date) >= timedelta(days=90)
        return True
