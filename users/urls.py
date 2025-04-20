from django.urls import path
from . import views  # assuming you have views

urlpatterns = [
    # Example path
    path('', views.home, name='home'),  # you can change this
]
