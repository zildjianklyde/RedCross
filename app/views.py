from django.shortcuts import render
from django.views.generic import TemplateView, ListView , DetailView
from django.views.generic.edit import CreateView, DeleteView,UpdateView
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy
from app.models import Database
# Create your views here.

class indexview(TemplateView):
    template_name = 'index.html'

class listview(ListView):
    model = Database
    context_object_name = 'items'
    fields = ['name','status','email','contact','blood','date']
    template_name = 'listview.html'

class createview(CreateView):
    model = Database
    fields = ['name','status','email','contact','blood','date']
    template_name = 'create.html'

class deleteview(DeleteView):
    model = Database
    template_name = 'delete.html'
    success_url = reverse_lazy('list')

class updateview(UpdateView):
    model = Database
    template_name = 'update.html'
    fields = ['name','status','email','contact','blood','date']
