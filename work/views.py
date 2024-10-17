from django.views.generic import TemplateView
from django.shortcuts import render

class HomeView(TemplateView):
    template_name = 'work/home.html'

def employeeList(request):
    return render(request, 'work/employeeList.html')