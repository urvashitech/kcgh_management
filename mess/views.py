from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from mess.models import MessBill
from mess.models import MonthlyMessSummary
from users.models import StudentInfo
from complaints.models import Complaint
from django.core.exceptions import MultipleObjectsReturned

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
    amount_spend = 0
    t_days = 0
    sum = 0
    per_day_charge = 0.0
    number_of_girls = User.objects.exclude(username__in=["warden", "matron","admin"]).count()
    constant_charge = 800
    if request.method == "POST":
        amount_spend = int(request.POST.get("s_amont"))
        t_days = int(request.POST.get("t_days"))

        if t_days == 0:
            messages.error(request, "Total days cannot be zero.")
        else:
            #calculating mess bill 
            sum = int(number_of_girls * constant_charge)
            per_day_charge = float( (amount_spend - sum) / t_days)

    print("Total number of girls are : ",number_of_girls)
    print("Total amount spent:", amount_spend)
    print("Total Number of days:",t_days)
    print("sum is : ", sum)
    print("Per day charge:", per_day_charge)
    month = datetime.now().strftime("%Y-%m")
    try:
            MonthlyMessSummary.objects.update_or_create(
                month_year=month,
                defaults={
                    "total_spent": amount_spend,
                    "total_days": t_days,
                    "number_of_girls": number_of_girls,
                    "per_day_charge": per_day_charge
                }
            )
    except MultipleObjectsReturned:
            return render(request, "404.html")

    return render(request,'calMessBill.html')

def editMessBill(request):
    print("🔥 View Called!")
    print("Method:", request.method)
    if request.method == "POST":
        print("✅ POST received")
        print("POST Data:", request.POST)
    else:
        print("👀 Not a POST request")
    
    '''if request.method == "POST":
        try:
            print("Inside POST request")
            name = request.POST.get("name")
            sch_no = request.POST.get("sch_no")
            days = int(request.POST.get("n_days"))
            g_amont = int(request.POST.get("g_amont"))

            print("Data from form:", name, sch_no, days, g_amont)

            previous_data = MessBill.objects.get(sch_no=sch_no)
            per_day_charge = MonthlyMessSummary.objects.get(
                month_year=datetime.now().strftime("%Y-%m")
            ).per_day_charge

            print("Per day charge is:", per_day_charge)

            total_amount = (per_day_charge * days) + g_amont

            MessBill.objects.create(
                user=previous_data.user,
                name=name,
                sch_no=sch_no,
                branch=previous_data.branch,
                category=previous_data.category,
                year=previous_data.year,
                number_of_days=days,
                total_amount=total_amount,
                dues=0,
                month_year=datetime.now().strftime("%Y-%m")
            )

            print("Mess Bill created successfully!")
            print("Mess Bill total is:", total_amount)

            messages.success(request, "Mess Bill successfully recorded!")
            return redirect("viewMessBill")  # 🧠 Use redirect if view name exists

        except MessBill.DoesNotExist:
            print("No previous record found for:", sch_no)
            messages.error(request, "No previous record found for this Scholar Number.")

        except Exception as e:
            print("Something went wrong:", e)'''

    print("Fallback: Showing form again.")
    return render(request, 'messBillForm.html')


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