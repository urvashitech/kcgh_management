from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=20)
    email = models.EmailField()
    category = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.name