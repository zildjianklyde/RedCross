from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Donor
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'donors/home.html'
    
    
def landing_page(request):
    return render(request, 'donors/landing_page.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'donors/register.html', {'form': form})

class DonorListView(ListView):
    model = Donor
    template_name = 'donors/donor_list.html'

class DonorCreateView(CreateView):
    model = Donor
    fields = ['name', 'blood_type', 'contact_info', 'last_donation_date']
    template_name = 'donors/donor_form.html'
    success_url = reverse_lazy('donor_list')

class DonorDetailView(DetailView):
    model = Donor
    template_name = 'donors/donor_detail.html'

class DonorUpdateView(UpdateView):
    model = Donor
    fields = ['name', 'blood_type', 'contact_info', 'last_donation_date']
    template_name = 'donors/donor_form.html'
    success_url = reverse_lazy('donor_list')

class DonorDeleteView(DeleteView):
    model = Donor
    template_name = 'donors/donor_confirm_delete.html'
    success_url = reverse_lazy('donor_list')
class LoginView(LoginView):
    template_name = 'donors/login.html'