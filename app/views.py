from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Donor, Database
from .forms import RegistrationForm
from .models import Donor
from .forms import EditDonorForm  

# Landing Page
def landing_page(request):
    return render(request, 'landing.html')

# Eligibility Check Page
def eligibility_check(request):
    return render(request, 'eligibility_check.html')

# Register View
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Hash the password
            user.save()
            Donor.objects.create(user=user, blood_type=form.cleaned_data['blood_type'])
            login(request, user)  # Log in after registration
            return redirect('donor_dashboard')
        else:
            messages.error(request, "Registration failed. Please check the form for errors.")
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

# Login View
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')  # Redirect admin to admin panel
            return redirect('donor_dashboard')  # Redirect donor to donor dashboard
        else:
            messages.error(request, "Invalid username or password.")

    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('landing')  # Redirect to landing page after logout

# Donor Dashboard
@login_required
def donor_dashboard(request):
    donor, created = Donor.objects.get_or_create(user=request.user)
    return render(request, 'donor_dashboard.html', {'donor': donor})

# Admin Dashboard
@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('donor_dashboard')
    donors = Donor.objects.all()
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
@login_required
def manage_users(request):
    if not request.user.is_superuser:
        return redirect('donor_dashboard')
    donors = Donor.objects.all()
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

@login_required
def delete_user(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    if request.method == 'POST':
        donor.user.delete()
        return redirect('manage_users')
    return render(request, 'admin_panel/delete_user.html', {'donor': donor})