from django.contrib import admin
from .models import Grocery, Vegetables, Extra, Constant  # Importing  model

admin.site.register(Grocery)  
admin.site.register(Vegetables) 
admin.site.register(Extra) 
admin.site.register(Constant)  
