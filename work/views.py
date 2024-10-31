from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.urls import reverse
from django.views.generic import TemplateView, ListView
from django.http import HttpResponseRedirect

from .date import CalculateDates
from .forms import EditForm
from .models import Attendance

@method_decorator(login_required, name='dispatch')
class HomeView(ListView):
    template_name = 'work/home.html'
    model = Attendance
    ordering = '-employee_number', '-date'
    date = CalculateDates()
    #初期値は今日の日付から年と月をとって文字列型で保持
    #calculate_days関数のformatが(年, 月)のためそれに合うように代入
    target_month = str(date.today.year) + str(date.today.month)
    #指定した月のquerysetが取れないときtemplateに渡すフラグ
    is_queryset = False

    def get(self, request, *args, **kwargs):
        self.is_queryset = False

        if 'drop_down' in self.request.GET:
            self.target_month = self.request.GET.get('drop_down')

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
    
    def post(self, request, *args, **kwargs):
        #ターゲットとなる年月をdate型で保持
        target_month = self.date.change_str_datetime(date=self.target_month)
        #年月とformからどの日のものかを取得して(年,月,日)のdate型を作成
        target_obj_date = self.date.change_datetime_from_post(target=target_month, date=self.request.POST['target-obj'])
        #target_obj_dateとpkをもとに対象のモデルを特定
        instance = Attendance.objects.get(employee_number=self.request.user.pk, date=target_obj_date)

        #対象のモデルをinstanceに指定したformインスタンスを作成
        form = EditForm(request.POST, instance=instance)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        #表示したい月のdatetime型objの取得
        target = self.date.change_str_datetime(date=self.target_month)

        #社員番号がログインしているユーザーのもので、出勤日がtargetの年月と一致しているものを取得
        queryset = queryset.filter(employee_number=self.request.user.pk, date__year=target.year, date__month=target.month)
        if queryset.first() is None:
            self.is_queryset = True

        return queryset
    
    def get_success_url(self):
        return str(reverse('work:home', kwargs={'pk':self.request.user.pk}))
    
    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(edit_form=form))
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        #表示している年月を取得
        context['target'] = self.date.change_str_datetime(date=self.target_month)
        #当月合わせて5か月分の過去の月を取得
        context['dropdown_months'] = self.date.calculate_five_month()
        #表示したい月の日数を取得
        context['date_list'] = self.date.localize_date_list(target_month=self.target_month)
        #object_listに入っているデータの日付だけのリスト
        context['queryset_days'] = self.get_day_from_queyset()
        context['is_queryset'] = self.is_queryset
        #編集モーダル内のform
        context['edit_form'] = EditForm()

        return context
    
    #querysetから日付のリストを作る
    def get_day_from_queyset(self):
        #querysetからdateフィールドだけのリストを作成
        queryset_dates = self.object_list.values_list('date', flat=True)
        queryset_dates_list = list(queryset_dates)

        #datetime型のobjから日付だけのリストを作る
        days_list = [date.day for date in queryset_dates_list ]
        return days_list

class EmployeeListView(TemplateView):
    template_name = 'work/employeeList.html'