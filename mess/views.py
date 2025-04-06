from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from mess.models import MessBill
from users.models import StudentInfo
from complaints.models import Complaint

from datetime import datetime
from django.db.models import Sum
# Create your views here.

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
    user_info = StudentInfo.objects.filter(user=request.user).first() 
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

    if request.method == "POST":
        guest_charge = float(request.POST.get("g_charge"))

    nuumber_of_girls = User.objects.count()
    constant_charge = 800
    total_days = (
    MessBill.objects.values('month_year').annotate(total_days=Sum('number_of_days')).order_by('month_year'))
    for entry in total_days:
        print(f"Month: {entry['month_year']}, Total Days: {entry['total_days']}")
        
    print("Total days for girls:", total_days)
    
    print("The guest charge is:", guest_charge)
    #calculating mess bill 
    month = datetime.now().strftime("%Y-%m")


    return render(request,'calMessBill.html')

def editMessBill(request):
    if request.method == "POST":
        name = request.POST.get("name")
        sch_no = request.POST.get("sch_no")
        days = int(request.POST.get("n_days"))
        

        try :
            previous_data = MessBill.objects.get(sch_no=sch_no)
            MessBill.objects.create(
                user=previous_data.user,
                name=name,
                sch_no=sch_no,
                branch=previous_data.branch,
                category=previous_data.category,
                year=previous_data.year,
                number_of_days=days,
                total_amount=0,  
                dues=0,  
                month_year=datetime.now().strftime("%Y-%m")
            )
            messages.success(request, "Mess Bill successfully recorded!")
            return render(request,"viewMessBill")
        except MessBill.DoesNotExist:
            messages.error(request, "No previous record found for this Scholar Number.")

    return render(request,'messBillForm.html')

def personalInfoForm(request):
    return render(request,'personalInfoForm.html')

def view_info(request):
    return render(request, 'viewInfo.html')

def viewMessBill(request):
    return render(request, 'viewMessBill.html')

def viewRecords(request):
    return render(request, 'viewRecords.html')

def viewStudentInfo(request):
    return render(request, 'viewStudentInfo.html')

def viewComplaints(request):
    return render(request, 'viewComplaints.html')



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