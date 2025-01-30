from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Donor, Database
from .forms import RegistrationForm, EditDonorForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .forms import DonorCreationForm

# Landing Page
def landing_page(request):
    return render(request, 'landing.html')

# Eligibility Check Page
def eligibility_check(request):
    return render(request, 'eligibility_check.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False  # Ensure regular users can't access admin
            user.save()
            Donor.objects.create(user=user, blood_type=form.cleaned_data['blood_type'])
            login(request, user)
            return redirect('donor_dashboard')
    # ... rest of the code ...
        else:
            messages.error(request, "Registration failed. Please check the form for errors.")
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            if user.is_superuser:
                return redirect('admin_dashboard')
            elif user.is_staff:  # If you need staff users
                return redirect('staff_dashboard')  
            else:
                return redirect('donor_dashboard')
    # ... rest of the code ...
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('landing')  # Redirect to landing page after logout


@login_required
def donor_dashboard(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    
    donor, created = Donor.objects.get_or_create(user=request.user)
    return render(request, 'donor_dashboard.html', {'donor': donor})

@staff_member_required
@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, "Unauthorized access!")
        return redirect('landing')
    
    # Get only donor accounts (exclude superusers)
    donors = Donor.objects.filter(user__is_superuser=False)
    return render(request, 'admin_dashboard.html', {'donors': donors})


@login_required
def profile(request):
    return redirect('donor_dashboard')  # Or create a dedicated profile page

# CRUD Views for Admin
class IndexView(TemplateView):
    template_name = 'index.html'

class ListView(ListView):
    model = Database
    context_object_name = 'items'
    fields = ['name', 'status', 'email', 'contact', 'blood', 'date']
    template_name = 'ListView.html'

class CreateView(CreateView):
    model = Database
    fields = ['name', 'status', 'email', 'contact', 'blood', 'date']
    template_name = 'create.html'

class DeleteView(DeleteView):
    model = Database
    template_name = 'delete.html'
    success_url = reverse_lazy('list')

class UpdateView(UpdateView):
    model = Database
    template_name = 'update.html'
    fields = ['name', 'status', 'email', 'contact', 'blood', 'date']

@staff_member_required
@login_required 
def manage_users(request):
    if not request.user.is_superuser:
        return redirect('donor_dashboard')
    
    # Exclude superusers from management
    donors = Donor.objects.filter(user__is_superuser=False)
    return render(request, 'admin_panel/manage_users.html', {'donors': donors})

@login_required
def edit_user(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    if request.method == 'POST':
        form = EditDonorForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = EditDonorForm(instance=donor)
    return render(request, 'admin_panel/edit_user.html', {'form': form})

@staff_member_required
@login_required
def delete_user(request, pk):
    if request.user.is_superuser:
        donor = get_object_or_404(Donor, pk=pk)
        if donor.user.is_superuser:
            messages.error(request, "Cannot delete superusers!")
            return redirect('manage_users')
def delete_user(request, pk):
    if not request.user.is_superuser:
        return redirect('donor_dashboard')
    
    donor = get_object_or_404(Donor, pk=pk)
    if donor.user.is_superuser:
        messages.error(request, "Cannot delete superusers!")
        return redirect('manage_users')
    
    if request.method == 'POST':
        donor.user.delete()
    return redirect('manage_users')

@login_required
def create_donor(request):
    if request.method == 'POST':
        form = DonorCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                Donor.objects.create(
                    user=user,
                    blood_type=form.cleaned_data['blood_type'],
                    last_donation_date=form.cleaned_data['last_donation_date'],
                    is_eligible=form.cleaned_data['is_eligible']
                )
                messages.success(request, "Donor created successfully!")
                return redirect('manage_users')
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
        else:
            messages.error(request, "Please correct the errors below")
    else:
        form = DonorCreationForm()
    
    return render(request, 'admin_panel/create_donor.html', {'form': form})


@login_required
def update_donor(request, id):
    donor = get_object_or_404(Donor, id=id)
    if request.method == 'POST':
        form = EditDonorForm(request.POST, instance=donor)
        if form.is_valid():
            try:
                updated_donor = form.save()
                updated_donor.update_eligibility()  # Ensure eligibility is updated
                messages.success(request, "Donor information updated successfully!")
                return redirect('admin_dashboard')
            except Exception as e:
                messages.error(request, f"Update failed: {str(e)}")
        else:
            print("Form errors:", form.errors)
            messages.error(request, "Please correct the errors below.")
    else:
        form = EditDonorForm(instance=donor)
    
    return render(request, 'admin_panel/update_donor.html', {'form': form})

@login_required
def delete_donor(request, id):
    donor = get_object_or_404(Donor, id=id)
    if request.method == 'POST':
        donor.delete()  # Delete the donor
        return redirect('admin_dashboard')  # Redirect to admin dashboard after deletion

    return render(request, 'admin_panel/delete_donor.html', {'donor': donor})
