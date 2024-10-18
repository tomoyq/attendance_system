from django.views.generic import TemplateView, ListView
from django.shortcuts import render

from .models import *

class HomeView(ListView):
    template_name = 'work/home.html'
    model = Attendance

class EmployeeListView(TemplateView):
    template_name = 'work/employeeList.html'