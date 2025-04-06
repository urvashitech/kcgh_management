from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from mess.models import MessBill
from users.models import User as CustomUser
from complaints.models import Complaint
from mess.forms import AdminProfileForm




def home(request):
    if request.user.is_authenticated:
        logout(request)  
    return render(request, "home.html")

@login_required
def messbill(request):
    mess_bill = MessBill.objects.filter(user=request.user).first()
    return render(request, "messbill.html", {'mess_bill': mess_bill, 'user': request.user})

def handleLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            admin_users = ["warden", "matron"]  # List of admin usernames
            if user.username in admin_users:  
                return redirect("manage_db")

            mess_bill = MessBill.objects.filter(user=request.user).first()
            return render(request, "studentProf.html", {"mess_bill": mess_bill})  

        else:
            return render(request, "404.html")

    return render(request, "home.html")

def handleLogOut(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect("home")

@login_required
def personalInfo(request):
    user_info = CustomUser.objects.filter(user=request.user).first() 
    if user_info is None:
        messages.error(request, "User data not found")
        return redirect("home")  

    return render(request, "personalInfo.html", {"user1": user_info, 'user': request.user})  

def staffInfo(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request, "staffInfo.html")

def studentInfo(request):
    return render(request, "studentProf.html")

def complain(request):
    if request.method == "POST":
        print("Received form data:", request.POST) 
        name = request.POST.get("name")
        email = request.POST.get("email")
        category = request.POST.get("category")
        description = request.POST.get("description")
        print("Extracted description:", description)

        if not description:
            messages.error(request, "Complaint description cannot be empty.")
            return redirect("complain")

        Complaint.objects.create(
            name=name,
            email=email,
            category=category,
            description=description
        )

        messages.success(request, "Your complaint has been submitted successfully.")
        return redirect("complain")

    print("Received form data:", request.POST)
    return render(request, "complain.html") 

@login_required
def manage_db(request):
    admin = ["warden", "matron"]
    if request.user.username in admin:
        return render(request, "manage_db.html", {"role": request.user.username})
    else:
        return render(request, "404.html")

def edit_page(request):
    return render(request, 'edit.html')

def calMessBill(request):
    return render(request, 'calMessBill.html')

def editMessBill(request):
    return render(request, 'messBillForm.html')

def personalInfoForm(request):
    return render(request, 'personalInfoForm.html')


@login_required
def create_admin_profile(request):
    if request.method == "POST":
        form = AdminProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Admin profile created successfully.")
            return redirect("home")  
    else:
        form = AdminProfileForm()
    return render(request, "adminProfile.html", {"form": form})
