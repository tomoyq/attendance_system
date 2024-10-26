from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import TemplateView, ListView

from .models import *
from .date import CalculateDates

@method_decorator(login_required, name='dispatch')
class HomeView(ListView):
    template_name = 'work/home.html'
    model = Attendance
    date = CalculateDates()
    #初期値は今日の日付から年と月をとって文字列型で保持
    #calculate_days関数のformatが(年, 月)のためそれに合うように代入
    target_month = str(date.today.year) + ', ' + str(date.today.month)

    def get(self, request, *args, **kwargs):

        if 'drop_down' in self.request.GET:
            self.target_month = self.request.GET['drop_down']

        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            if self.get_paginate_by(self.object_list) is not None and hasattr(
                self.object_list, "exists"
            ):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(
                    _("Empty list and “%(class_name)s.allow_empty” is False.")
                    % {
                        "class_name": self.__class__.__name__,
                    }
                )
        context = self.get_context_data()
        return self.render_to_response(context)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        #当月合わせて5か月分の過去の月を取得
        context['dropdown_months'] = self.date.calculate_five_month()
        #表示したい月の日数を取得
        context['date_list'] = self.date.localize_date_list(target_month=self.target_month)

        return context

class EmployeeListView(TemplateView):
    template_name = 'work/employeeList.html'