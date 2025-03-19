from django.db import models

# Create your models here.
class Grocery(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    amount = models.FloatField()
    rate = models.FloatField()

    def __str__(self):
        return self.name
    

class Vegetables(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    amount = models.FloatField()
    rate = models.FloatField()

    def __str__(self):
        return self.name
    
class Extra(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    amount = models.FloatField()
    rate = models.FloatField()

    def __str__(self):
        return self.name
    
class Constant(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    rate = models.FloatField()

    def __str__(self):
        return self.name    