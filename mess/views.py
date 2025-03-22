from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "home.html")

def messbill(request):
    return render(request, "messbill.html")

def personalInfo(request):
    return render(request, "personalInfo.html")

def staffInfo(request):
    return render(request, "staffInfo.html")

def studentInfo(request):
    return render(request, "studentProf.html")

def complain(request):  
    return render(request, "complain.html")