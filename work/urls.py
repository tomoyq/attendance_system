from django.urls import path

from . import views

urlpatterns = [
     #'/<int:userId>'
    path('', views.index, name='home'),
    #'/admin/<int:userId>'
    path('admin/', views.employeeList, name='employeeList'),
]