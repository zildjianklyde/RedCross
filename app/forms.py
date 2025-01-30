from django import forms
from django.contrib.auth.models import User
from .models import Donor
from django.core.mail import send_mail
from datetime import date, timedelta
from django.contrib.auth.forms import UserCreationForm
from .models import Donor, User

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    blood_type = forms.ChoiceField(choices=[
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ], label="Blood Type")
    last_donation_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    is_eligible = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'blood_type']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match.")
            
def send_donation_reminders():
    donors = Donor.objects.all()
    for donor in donors:
        if donor.last_donation_date and (date.today() - donor.last_donation_date) >= timedelta(days=90):
            send_mail(
                'Blood Donation Reminder',
                'You are eligible to donate blood again. Please visit our center.',
                'noreply@redcross.com',
                [donor.user.email],
                fail_silently=False,
            )
class EditDonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['blood_type', 'last_donation_date', 'is_eligible']
        widgets = {
            'last_donation_date': forms.DateInput(attrs={'type': 'date'})
        }

class DonorCreationForm(UserCreationForm):
    blood_type = forms.ChoiceField(
       choices=Donor.BLOOD_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    last_donation_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    is_eligible = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'blood_type', 'last_donation_date', 'is_eligible']