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

class RegistrationForm(UserCreationForm):
    blood_type = forms.ChoiceField(
        choices=Donor.BLOOD_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    email = forms.EmailField(required=True)

    last_donation_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'blood_type']


class EditDonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['blood_type', 'last_donation_date', 'is_eligible']
        widgets = {
            'last_donation_date': forms.DateInput(attrs={'type': 'date'})
        }

class EligibilityForm(forms.Form):
    age = forms.BooleanField(
        label="Are you between 17-65 years old?",
        required=True,
        widget=forms.RadioSelect(choices=[(True, "Yes"), (False, "No")])
    )
    weight = forms.BooleanField(
        label="Do you weigh at least 50kg (110 lbs)?",
        required=True,
        widget=forms.RadioSelect(choices=[(True, "Yes"), (False, "No")])
    )
    
    # Health Status
    current_health_issues = forms.MultipleChoiceField(
        label="Do you currently have any of these?",
        required=False,
        choices=[
            ('fever', 'Fever/cold/cough'),
            ('wounds', 'Open wounds/skin infections'),
            ('pregnancy', 'Pregnancy (current or recent 6 months)'),
        ],
        widget=forms.CheckboxSelectMultiple
    )
    
    # Medical History
    medical_history = forms.MultipleChoiceField(
        label="Have you ever had:",
        required=False,
        choices=[
            ('hiv', 'HIV/AIDS or positive HIV test'),
            ('ebola', 'Ebola/malaria (last 3 years)'),
            ('transplant', 'Organ transplant (last 3 months)'),
        ],
        widget=forms.CheckboxSelectMultiple
    )
    
    # Recent Activities
    recent_activities = forms.MultipleChoiceField(
        label="In the last 3 months have you:",
        required=False,
        choices=[
            ('tattoo', 'Had a tattoo/piercing'),
            ('travel', 'Traveled to malaria-risk areas'),
            ('medication', 'Taken blood thinners'),
        ],
        widget=forms.CheckboxSelectMultiple
    )

class DonorForm(forms.ModelForm):
    last_donation_date = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    blood_type = forms.ChoiceField(
        choices=Donor.BLOOD_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Donor
        fields = ['blood_type', 'last_donation_date']

class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['user', 'blood_type', 'last_donation_date']

    # Customize fields to add placeholders
    user = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    last_donation_date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    blood_type = forms.ChoiceField(choices=Donor.BLOOD_TYPE_CHOICES)