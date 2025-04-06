from django.db import models
from django.contrib.auth.models import User
# Create your models here.    
class StudentInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    sch_no = models.IntegerField()
    branch = models.CharField(max_length=100)
    year = models.IntegerField()
    category = models.CharField(max_length=15)
    dob = models.DateField()
    blood_group = models.CharField(max_length=5)
    email = models.EmailField()
    address = models.CharField(max_length=100)
    phone = models.IntegerField(max_length=10)
    g_no = models.IntegerField(max_length=10)
    g_name = models.CharField(max_length=100)
    g_email = models.EmailField(max_length=30)
    g_occupation = models.CharField(max_length=100)
    g_address = models.CharField(max_length=100)
    e_no = models.IntegerField(max_length=10)
    l_name = models.CharField(max_length=100)
    l_address = models.CharField(max_length=100)
    l_no = models.IntegerField(max_length=10)
    disease = models.CharField(max_length=100)


    def __str__(self):
        return self.name