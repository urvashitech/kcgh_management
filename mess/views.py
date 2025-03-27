from django.shortcuts import render , redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from mess.models import MessBill
from users.models import User as CustomUser
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def home(request):
    return render(request, "home.html")

@login_required
def messbill(request):

    mess_bill = MessBill.objects.filter(user=request.user).first()
    return render(request, "messbill.html" , {'user' : mess_bill})


def handleLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")

            mess_bill = MessBill.objects.filter(user=request.user).first()

            # ✅ Using render() to pass data without changing URL
            return render(request, "studentProf.html", {"mess_bill": mess_bill})  

        else:
            messages.error(request, "Invalid Credentials")
            return render(request, "home.html")

    return render(request, "home.html")

def handleLogOut(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect("home")

@login_required
def personalInfo(request):
    user_info = CustomUser.objects.filter(username=request.user.username).first()  # ✅ Corrected Query
    if user_info is None:
        messages.error(request, "User data not found")
        return redirect("home")  # Redirect to home if user data is missing

    return render(request, "personalInfo.html", {"user": user_info})  # ✅ Pass actual user instance


def staffInfo(request):
    return render(request, "staffInfo.html")

def studentInfo(request):
    return render(request, "studentProf.html")

def complain(request):  
    return render(request, "complain.html")