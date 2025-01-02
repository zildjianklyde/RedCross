from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Donor
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView  # Using Django's built-in LoginView and LogoutView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView

# Login view to handle authentication
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to the homepage if the user is already logged in

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to a protected page like 'home' or 'dashboard'
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    
    return render(request, 'donors/login.html', {'form': form})

# Home view
class HomeView(TemplateView):
    template_name = 'donors/home.html'

# Landing page view
def landing_page(request):
    return render(request, 'donors/landing_page.html')

# Register view to handle user registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'donors/register.html', {'form': form})

# Donor List view
class DonorListView(ListView):
    model = Donor
    template_name = 'donors/donor_list.html'

# Donor Create view
class DonorCreateView(CreateView):
    model = Donor
    fields = ['name', 'blood_type', 'contact_info', 'last_donation_date']
    template_name = 'donors/donor_form.html'
    success_url = reverse_lazy('donor_list')

# Donor Detail view
class DonorDetailView(DetailView):
    model = Donor
    template_name = 'donors/donor_detail.html'

# Donor Update view
class DonorUpdateView(UpdateView):
    model = Donor
    fields = ['name', 'blood_type', 'contact_info', 'last_donation_date']
    template_name = 'donors/donor_form.html'
    success_url = reverse_lazy('donor_list')

# Donor Delete view
class DonorDeleteView(DeleteView):
    model = Donor
    template_name = 'donors/donor_confirm_delete.html'
    success_url = reverse_lazy('donor_list')

# Use the built-in LogoutView for logout functionality
def login_view(request):
    # If the user is already logged in, redirect to the homepage or dashboard
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to 'home' page or wherever you want

    # Handle the login form submission
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to 'home' page or wherever you want
    else:
        form = AuthenticationForm()

    return render(request, 'donors/login.html', {'form': form})