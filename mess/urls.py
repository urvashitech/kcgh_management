
from django.urls import path , include
from mess import views
urlpatterns = [
    path("", views.home, name="home"),
    path("messbill/<str:month>/", views.messbill, name="messbill"),
    path('handleLogin/', views.handleLogin, name='handleLogin'),
    path('handleLogOut/', views.handleLogOut, name='handleLogOut'),   
    path("personalInfo", views.personalInfo, name="personalInfo"),
    path("staffInfo", views.staffInfo, name="staffInfo"),
    path("studentInfo", views.studentInfo, name="studentInfo"),
    path("complain", views.complain, name="complain"), 
    path("manage_db",views.manage_db, name="manage_db"),
    path("edit",views.edit_page,name='edit'),
    path('calMessBill',views.calMessBill,name='calMessBill'),
    path('testEditBill', views.testEditBill, name='testEditBill'),
    path("personalInfoForm",views.personalInfoForm, name="personalInfoForm"),
    path('view-info', views.view_info, name='view_info'),
    path('viewRecords', views.viewRecords, name='viewRecords'),
    path('viewStudentInfo', views.view_student_list, name='viewStudentInfo'),
    path('viewComplaints', views.viewComplaints, name='viewComplaints'),
    path('viewMessBill', views.viewMessBill, name='viewMessBill'),
    path('monthWiseBill', views.monthWiseBill, name='monthWiseBill'),
    path('monthlyBill/<str:month>/', views.monthly_bill, name='monthly_bill'),
    path('students/<int:student_id>/', views.student_detail, name='student_detail'),
]
