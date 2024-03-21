from django.db import models

# Create your models here.

class Inventory(models.Model): 
    id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=255) 
    category = models.CharField(max_length=100) 
    price = models.IntegerField() 
    discount = models.IntegerField()
    quantity = models.IntegerField() 
    barcode = models.IntegerField(unique=True)

    def str(self):
        return self.name

