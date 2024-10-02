from django.shortcuts import render

def index(request):
    return render(request, 'work/home.html')

def employeeList(request):
    return render(request, 'work/employeeList.html')