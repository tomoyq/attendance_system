from django.urls import path

from . import views

app_name = 'work'

urlpatterns = [
     #'/<int:userId>'
    path('', views.HomeView.as_view(), name='home'),
    #'/admin/<int:userId>'
    path('admin/', views.employeeList, name='employeeList'),
]