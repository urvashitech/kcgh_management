from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.
class MessBill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    s_no = models.IntegerField()
    name = models.CharField(max_length=50)
    sch_no = models.IntegerField()
    category = models.CharField(max_length=15)
    branch = models.CharField(max_length=15)
    year = models.IntegerField()
    number_of_days = models.IntegerField(default=10)
    total_amount = models.IntegerField()
    dues = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.user and MessBill.objects.filter(user=self.user).exists() and not self.pk:
            raise ValidationError("A MessBill for this user already exists.")
        super().save(*args, **kwargs)

    @property
    def display_year(self):
        """Returns 'Final' for 4th-year students, otherwise returns year number."""
        return "Final" if self.year == 4 else f"{self.year}rd" if self.year == 3 else f"{self.year}nd" if self.year == 2 else f"{self.year}st"

    def __str__(self):
        return self.name



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    room_number = models.CharField(max_length=10, blank=True)
    contact_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
