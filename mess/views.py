from mess.models import MessBill
from mess.models import MonthlyMessSummary
from users.models import StudentInfo
from complaints.models import Complaint
from users.models import ArchivedMessBill
from django.shortcuts import render , redirect 
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
import calendar
from django.core.exceptions import MultipleObjectsReturned
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from complaints.models import Complaint
from django.utils import timezone
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy


from django.db.models import Sum
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        logout(request)  
    return render(request, "home.html")


@login_required
def messbill(request, month):
    print("Month from URL:", month)

    try:
        month_number = list(calendar.month_name).index(month)  
    except ValueError:
        return HttpResponse("Invalid month")

    current_year = datetime.now().year
    formatted_month = f"{current_year}-{month_number:02d}"  

    mess_bill = MessBill.objects.filter(user=request.user, month_year=formatted_month).first()

    print("Filtered mess bill:", mess_bill)

    return render(request, "messbill.html", {
        'mess_bill': mess_bill,
        'user': request.user,
        'month': month,
        'bills': bool(mess_bill),
    })


def handleLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            admin_users = ["warden", "matron"]  
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
        return render(request,"404.html")  

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


def testEditBill(request):
    user = request.user
    name = ""
    sch_no = 0
    n_days = 0
    g_amont = 0
    constant_charge = 800 
    total_amount = 0

    if request.method == "POST":
       
        name = request.POST.get("name")
        sch_no = request.POST.get("sch_no")
        n_days = request.POST.get("n_days")
        g_amont = request.POST.get("g_amont")

        
        if name and sch_no and n_days and g_amont:
            n_days = int(n_days)
            g_amont = int(g_amont)
            sch_no = int(sch_no)
            month_year = datetime.now().strftime("%Y-%m")

            per_day_charge = MonthlyMessSummary.objects.filter(month_year=datetime.now().strftime("%Y-%m")).values('per_day_charge').first()

            if  per_day_charge.get('per_day_charge', 0) > 0:
                per_day_charge = float(per_day_charge['per_day_charge']) 
                total_amount = (n_days * per_day_charge) + (constant_charge + g_amont)
            print("The per day charge is: ", per_day_charge)
            print("The total amount is: ", total_amount)

            if MessBill.objects.filter(sch_no=sch_no, month_year=month_year).exists():
                messages.error(request, "A MessBill for this student already exists for this month.")
                return render(request, "messBillForm.html")

            try:
                bill = MessBill.objects.get(sch_no=sch_no)
            except MessBill.DoesNotExist:
                messages.error(request, "Student profile not found for this sch_no.")
                return render(request, "messBillForm.html")
            mess_bill = MessBill(
                user = bill.user,
                name=name,
                sch_no=sch_no,
                category=bill.category,
                branch=bill.branch,
                year=bill.year,
                number_of_days=n_days,
                total_amount=total_amount,
                dues=bill.dues,
                month_year=month_year,
            )
            try:
                mess_bill.save()
                messages.success(request, "Mess Bill saved successfully.")
            except ValidationError as e:
                messages.error(request, str(e))    
                
        else:
            messages.error(request, "Please fill all the required fields.")        
        
    return render(request, "messBillForm.html")



def personalInfoForm(request):
    name = ""
    sch_no = 0
    branch = ""
    year = 0
    category = ""
    dob = ""
    blood_group = ""
    email = ""
    address = ""
    phone = ""
    g_no = ""
    g_name = ""
    g_email = ""
    g_occupation = ""
    g_address = ""
    e_no = ""
    l_name = ""
    l_address = ""
    l_no = 0
    disease = ""
    if request.method =="POST":
        name = request.POST.get("name")
        sch_no = request.POST.get("sch_no")
        branch = request.POST.get("branch")
        year = request.POST.get("year")
        category = request.POST.get("category")
        dob = request.POST.get("dob")
        blood_group = request.POST.get("blood_group")
        email = request.POST.get("email")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        g_no = request.POST.get("g_no")
        g_name = request.POST.get("g_name")
        g_email = request.POST.get("g_email")
        g_occupation = request.POST.get("g_occupation")
        g_address = request.POST.get("g_address")
        e_no = request.POST.get("e_no")
        l_name = request.POST.get("l_name")
        l_address = request.POST.get("l_address")
        l_no = request.POST.get("l_no")
        disease = request.POST.get("disease")

        try:
            user = User.objects.get(username = sch_no)
        except User.DoesNotExist:
            messages.error(request, "User profile not found for this sch_no.")
            return render(request, "personalInfoForm.html")

        studentInfo = StudentInfo.objects.create(
            user = user,
            name = name,
            sch_no = sch_no,
            branch = branch,
            year = year,
            category = category,
            dob = dob,
            blood_group = blood_group,
            email = email,
            address = address,
            phone = phone,
            g_no = g_no,
            g_name = g_name,
            g_email = g_email,
            g_occupation = g_occupation,
            g_address = g_address,
            e_no = e_no,
            l_name = l_name,
            l_address = l_address,
            l_no = l_no,
            disease = disease,

        )
        try:
                studentInfo.save()
                messages.success(request, "Mess Bill saved successfully.")
        except ValidationError as e:
                messages.error(request, str(e))    

        messages.success(request, "Your complaint has been submitted successfully.")
        return redirect("personalInfoForm")
    
 

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


def monthly_bill(request):
    return render(request, 'monthly_bill.html')


def editMessBill(request):
    return render(request, 'messBillForm.html')


def monthly_bill(request, month):
    month = month.capitalize()
    month_number = list(calendar.month_name).index(month) if month in calendar.month_name else None

    if not month_number:
        return render(request, 'monthly_bill.html', {'bills': []})

    current_year = datetime.now().year
    formatted_month_year = f"{current_year}-{month_number:02d}"
    excluded_users = User.objects.exclude(username__in=["warden", "matron", "admin"])
    bills = MessBill.objects.filter(
    user__in=excluded_users,
    month_year=formatted_month_year
        ).order_by("-year", "name")

    return render(request, 'monthly_bill.html', {'bills': bills}, )

def monthWiseBill(request):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']
    
    if request.method == "POST":
        selected_month = request.POST.get("month")
        if selected_month:
            return redirect(reverse('messbill', kwargs={'month': selected_month}))
    
    return render(request, 'monthWiseBill.html', {'months': months})

def viewMessBill(request):
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    
    if request.method == "POST":
        selected_month = request.POST.get('month')
        if selected_month:
            url = reverse('monthly_bill', kwargs={'month': selected_month})
            return redirect(url)
    
    return render(request, 'viewMessBill.html', {'months': months})

def view_student_list(request):
    students = StudentInfo.objects.all()
    return render(request, 'viewStudentInfo.html', {'students': students})

def student_detail(request, student_id):
    student = get_object_or_404(StudentInfo, id=student_id)
    return render(request, 'student_detail.html', {'student': student})


def viewComplaints(request):
    status_filter = request.GET.get("status")

    if status_filter == "solved":
        complaints = Complaint.objects.filter(is_solved=True)
    elif status_filter == "unsolved":
        complaints = Complaint.objects.filter(is_solved=False)
    else:
        complaints = Complaint.objects.all()

    return render(request, "viewComplaints.html", {"complaints": complaints})


def toggle_status(request, pk):
    complaint = Complaint.objects.get(pk=pk)
    complaint.is_solved = not complaint.is_solved

    if complaint.is_solved:
        complaint.solved_at = timezone.now()
    else:
        complaint.solved_at = None

    complaint.save()
    return redirect('viewComplaints')

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'auth/change_password.html'
    success_url = reverse_lazy('password_change_done')


def archive_old_record():
    today = datetime.today()
    
    # Run only on December 31st
    if today.month == 12 and today.day == 31:
        old_records = StudentInfo.objects.filter(year=today.year)
        archived_records = []

        for record in old_records:
            archived_records.append(ArchivedMessBill(
                user=record.user,
                name=record.name,
                sch_no=record.sch_no,
                branch=record.branch,
                year=record.year,
                category=record.category,
                dob=record.dob,
                blood_group=record.blood_group,
                email=record.email,
                address=record.address,
                phone=record.phone,
                g_no=record.g_no,
                g_name=record.g_name,
                g_email=record.g_email,
                g_occupation=record.g_occupation,
                g_address=record.g_address,
                e_no=record.e_no,
                l_name=record.l_name,
                l_address=record.l_address,
                l_no=record.l_no,
                disease=record.disease,
            ))

        ArchivedMessBill.objects.bulk_create(archived_records)

        
        old_records.delete()
    else:
        print("Not the end of the year. Skipping archival.")
