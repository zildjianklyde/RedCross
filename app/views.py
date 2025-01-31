from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import Donor, Database
from .forms import RegistrationForm, EditDonorForm, DonorForm, UserCreationForm, EligibilityForm

# ✅ Landing Page
def landing_page(request):
    return render(request, 'landing.html')

# ✅ Eligibility Check
def eligibility_check(request):
    if request.method == 'POST':
        form = EligibilityForm(request.POST)
        if form.is_valid():
            request.session['eligible'] = is_eligible(form.cleaned_data)
            if request.session['eligible']:
                return redirect('register')
            else:
                messages.error(request, "Based on your answers, you're not currently eligible to donate blood.")
                return redirect('landing')
    else:
        form = EligibilityForm()
    return render(request, 'eligibility_check.html', {'form': form})

def is_eligible(cleaned_data):
    """Determine eligibility based on form data"""
    if not cleaned_data['age'] or not cleaned_data['weight']:
        return False
    if any([cleaned_data['current_health_issues'], cleaned_data['medical_history'], cleaned_data['recent_activities']]):
        return False
    return True

# ✅ Registration View (Fixed)
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            donor = Donor.objects.create(user=user, blood_type=form.cleaned_data['blood_type'])
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('donor_dashboard')
        else:
            messages.error(request, "Registration failed. Please check the form for errors.")
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

# ✅ Login View (Fixed)
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
                return redirect('index')
            return redirect('donor_dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# ✅ Logout View
def logout_view(request):
    logout(request)
    return redirect('landing')

# ✅ Donor Dashboard (Fixed)
@login_required
def donor_dashboard(request):
    donor, created = Donor.objects.get_or_create(user=request.user)
    return render(request, 'donor_dashboard.html', {'donor': donor})

# ✅ Admin Dashboard (Fixed)
@staff_member_required
@login_required
def admin_dashboard(request):
    donors = Donor.objects.all()
    return render(request, 'admin_dashboard.html', {'donors': donors})

# ✅ Profile View
@login_required
def profile(request):
    return render(request, 'profile.html')

# ✅ Manage Users (Fixed)
@staff_member_required
@login_required
def manage_users(request):
    donors = Donor.objects.all()
    return render(request, 'admin_panel/manage_users.html', {'donors': donors})

# ✅ Create Donor (Fixed)
@staff_member_required
@login_required
def create_donor(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            donor = form.save()
            Donor.objects.create(user=user, blood_type=form.cleaned_data['blood_type'])
            messages.success(request, "Donor created successfully!")
            return redirect('list')
        else:
            messages.error(request, "Please correct the errors below")
    else:
        form = UserCreationForm()
    return render(request, 'admin_panel/create_donor.html', {'form': form})

# ✅ Edit Donor (Fixed)
@staff_member_required
@login_required
def edit_donor(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    if request.method == 'POST':
        form = EditDonorForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            messages.success(request, "Donor updated successfully!")
            return redirect('index')
    else:
        form = EditDonorForm(instance=donor)
    return render(request, 'admin_panel/edit_donor.html', {'form': form})

# ✅ Delete Donor (Fixed)
@staff_member_required
@login_required
def update_donor(request, id):
    donor = get_object_or_404(Donor, id=id)
    if request.method == 'POST':
        form = EditDonorForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            messages.success(request, "Donor updated successfully!")
            return redirect('index')  # Redirect to admin dashboard after update
        else:
            messages.error(request, "Update failed. Please check the form.")
    else:
        form = EditDonorForm(instance=donor)
    
    return render(request, 'admin_panel/update_donor.html', {'form': form})

@login_required
def delete_donor(request, id):
    donor = get_object_or_404(Donor, id=id)
    if request.method == 'POST':
        donor.delete()  # Delete the donor
        messages.success(request, "Donor deleted successfully!")
        return redirect('index')  # Redirect after deletion

    return render(request, 'admin_panel/delete_donor.html', {'donor': donor})

# ✅ CRUD Views (Fixed)
class listview(ListView):
    model = Database
    context_object_name = 'items'
    template_name = 'listview.html'

class createview(CreateView):
    model = Donor
    form_class = DonorForm
    template_name = 'create.html'
    success_url = reverse_lazy('list')

class deleteview(DeleteView):
    model = Database
    template_name = 'delete.html'
    success_url = reverse_lazy('list')

class updateview(UpdateView):
    model = Database
    template_name = 'update.html'
    fields = ['name', 'status', 'email', 'contact', 'blood', 'date']

@staff_member_required
@login_required
def index(request):
    if not request.user.is_superuser:
        messages.error(request, "Unauthorized access!")
        return redirect('donor_dashboard')
    
    # Get all donor accounts (exclude superusers)
    donors = Donor.objects.filter(user__is_superuser=False)
    return render(request, 'index.html', {'donors': donors})
