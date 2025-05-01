from django.db import models
from django.contrib.auth.models import User

class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=20)
    email = models.EmailField()
    category = models.CharField(max_length=20)
    description = models.TextField()
    is_solved = models.BooleanField(default=False)
    date_of_complaint = models.DateField(auto_now_add=True)
    date_of_action = models.DateField(null=True, blank=True)
    solved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
