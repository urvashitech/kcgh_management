
from django.urls import path , include
from mess import views
urlpatterns = [
    path("", views.home, name="home"),
    path("messbill", views.messbill, name="messbill"),
    path('handleLogin/', views.handleLogin, name='handleLogin'),
    path('handleLogOut/', views.handleLogOut, name='handleLogOut'),   
    path("personalInfo", views.personalInfo, name="personalInfo"),
    path("staffInfo", views.staffInfo, name="staffInfo"),
    path("studentInfo", views.studentInfo, name="studentInfo"),
    path("complain", views.complain, name="complain"), 
    path("manage_db",views.manage_db, name="manage_db"),
    path("edit",views.edit_page,name='edit'),
    path('calMessBill',views.calMessBill,name='calMessBill'),
    path('editMessBill',views.editMessBill,name='editMessBill'),
    path("personalInfoForm",views.personalInfoForm, name="personalInfoForm"),
]
