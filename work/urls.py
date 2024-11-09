from django.urls import path

from . import views

app_name = 'work'

urlpatterns = [
    #勤怠一覧ページ
    path('<int:pk>', views.HomeView.as_view(), name='home'),
    #管理者の社員一覧ページ
    path('admin/<int:managerId>', views.EmployeeListView.as_view(), name='employeeList'),
]