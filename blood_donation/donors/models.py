from django.db import models

class Donor(models.Model):
    name = models.CharField(max_length=100)
    blood_type = models.CharField(max_length=3)
    contact_info = models.CharField(max_length=255)
    last_donation_date = models.DateField()

    def __str__(self):
        return self.name
