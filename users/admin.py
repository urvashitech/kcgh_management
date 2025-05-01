from django.contrib import admin
from .models import StudentInfo 
from .models import ArchivedMessBill

# Register your models here.
admin.site.register(StudentInfo)
admin.site.register(ArchivedMessBill)