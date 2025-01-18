from django.db import models
from django.urls import reverse
# Create your models here.

class database(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    blood = models.CharField(max_length=100)
    date = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse("list")
    