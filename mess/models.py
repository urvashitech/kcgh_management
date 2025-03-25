from django.db import models

# Create your models here.
class MessBill (models.Model):
    s_no = models.IntegerField()
    name = models.CharField(max_length=50)
    sch_no = models.IntegerField()
    category = models.CharField(max_length=15)
    branch = models.CharField(max_length=15)
    year = models.IntegerField()
    number_of_days = models.IntegerField(default=10)
    total_amount = models.IntegerField()
    dues = models.IntegerField(default= 0)

 

    @property
    def display_year(self):
        """Returns 'Final' for 4th-year students, otherwise returns year number."""
        return "Final" if self.year == 4 else f"{self.year}rd" if self.year == 3 else f"{self.year}nd" if self.year == 2 else f"{self.year}st"
       

    def __str__(self):
        return self.name