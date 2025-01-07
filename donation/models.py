from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    blood_type = models.CharField(max_length=3, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')])
    last_donation_date = models.DateField(blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Changed related_name to avoid conflicts
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Changed related_name to avoid conflicts
        blank=True
    )
class Eligibility(models.Model):
    condition = models.CharField(max_length=255)
    is_eligible = models.BooleanField(default=True)
    def __str__(self):
        return self.condition

class Donation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_donated = models.DateField()