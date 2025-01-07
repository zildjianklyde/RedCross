from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Donor

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
