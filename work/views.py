from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView

from .models import *

@method_decorator(login_required, name='dispatch')
class HomeView(ListView):
    template_name = 'work/home.html'
    model = Attendance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class EmployeeListView(TemplateView):
    template_name = 'work/employeeList.html'