
from django.urls import path , include
from mess import views
urlpatterns = [
    path("", views.landing_page, name="home"),
    path("messbill", views.messbill, name="messbill"),
    path("personalInfo", views.personalInfo, name="personalInfo"),
    path("staffInfo", views.staffInfo, name="staffInfo"),
    path("studentInfo", views.studentInfo, name="studentInfo"),
    path("complain", views.complain, name="complain"), 
]
