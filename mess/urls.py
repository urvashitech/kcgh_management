
from django.urls import path , include
from mess import views
urlpatterns = [
    path("", views.home, name="home"), 
]
