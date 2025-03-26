
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
]
