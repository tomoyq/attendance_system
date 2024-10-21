from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView

from .models import *

@method_decorator(login_required, name='dispatch')
class HomeView(ListView):
    template_name = 'work/home.html'
    model = Attendance

class EmployeeListView(TemplateView):
    template_name = 'work/employeeList.html'