from django.db import models

# Create your models here.
class User(models.Model):
    email= models.CharField(max_length=100, unique=True)
    name= models.CharField(max_length=100)
    cardNumber= models.CharField(max_length=16, unique=True)
    password= models.CharField(max_length=100)
    address= models.CharField(max_length=100)
    
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Invoice(models.Model):
    """ This is a invoice in visa service """
    itemName = models.CharField(max_length = 255)
    quantity = models.IntegerField()
    itemPrice = models.IntegerField()
    cost = models.IntegerField()

    def __str__(self):
        return self.itemName
