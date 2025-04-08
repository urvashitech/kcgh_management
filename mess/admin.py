from django.contrib import admin
from .models import MessBill  # Import your model
from .models import MonthlyMessSummary 

admin.site.register(MessBill)  # Register the model 
admin.site.register(MonthlyMessSummary)