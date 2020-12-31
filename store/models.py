from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db.models import CASCADE, SET_NULL
from django.db.models.signals import pre_save
from django.forms.widgets import MultipleHiddenInput
from medicalstore.util import *
# from django_countries.fields import CountryField


class Customer(models.Model):
    user=models.OneToOneField(User, on_delete=CASCADE, null=True, blank=True)
    name=models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    discription = models.TextField(default=False,blank=False)
    digital=models.BooleanField(default=False, blank=False)
    image=models.ImageField(null=True, blank=True)
    slug=models.SlugField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name
    

     #if no image then it will so no image instead of throwing error if u use imageurl function
    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url



    


class Meta:
    ordering=('publishrd_at',)



def pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug=unique_slug_generator(instance)

pre_save.connect(pre_save_receiver,sender=Product)


   




class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id=models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.id)


    # @property
    # def shipping(self):
    #     shipping=False
    #     orderitems=self.orderitem_set.all()
    #     for i in orderitems:
    #         if i.product.digital==False:
    #             shipping=True
    #     return shipping

    #SUBTOTAL
    # @property
    # def get_cart_total(self):
    #     orderitems = self.orderitem_set.all()
    #     total = sum([item.get_total for item in orderitems])
    #     return int(total)
    #NO OF ITEM IN CART
    @property
    def get_cart_items(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.quantity for item in orderitems])
        return total
    #GRAND TOTAL
    # @property
    # def get_grand_total(self):
    #     orderitems=self.orderitem_set.all()
    #     total=sum([item.get_total for item in orderitems])
    #     gst=total*(5/100)
    #     grand_total=int(total+gst)
    #     return grand_total
    
   
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=SET_NULL, null=True, blank=True)
    quantity=models.IntegerField(default=0, null=True, blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    # @property
    # def get_total(self):
        
    #     total= self.product.price * self.quantity
    #     return total


    

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True)
    zip_add = models.CharField(max_length=200, null=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return self.customer



class Contact(models.Model):
    sno= models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=100)
    msg=models.TextField()
    timespam=models.DateTimeField(auto_now_add=True, blank=True)
  

    def __str__(self):
        return self.name
    