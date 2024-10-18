from django.urls import path

from . import views

app_name = 'work'

urlpatterns = [
    path('<int:pk>', views.HomeView.as_view(), name='home'),
    #'/admin/<int:userId>'
    path('admin/', views.EmployeeListView.as_view(), name='employeeList'),
]