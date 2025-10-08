from django.db import models
import os
import datetime
from django.contrib.auth.models import User


def getFileName(request, filename):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    new_filename = f"{now_time}{filename}"
    return os.path.join('uploads/', new_filename)



class Category(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)   # category name
    image = models.ImageField(upload_to=getFileName, null=True, blank=True)  # optional image
    description = models.TextField(max_length=500, null=False, blank=False)  # details about category
    status = models.BooleanField(default=False, help_text="0-show, 1-Hidden")  # visible/hidden switch
    created_at = models.DateTimeField(auto_now_add=True)   # first created timestamp
    updated_at = models.DateTimeField(auto_now=True)       # last modified timestamp

    def __str__(self):
        return self.name
    

class products(models.Model):
    category= models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=False, blank=False)   
    vendor = models.CharField(max_length=150, null=False, blank=False)  
    product_image = models.ImageField(upload_to=getFileName, null=False, blank=False) 
    quantity = models.IntegerField( null=False, blank=False) 
    original_price = models.FloatField( null=False, blank=False)
    selling_price = models.FloatField( null=False, blank=False)
    description = models.TextField(max_length=500, null=False, blank=False)  
    status = models.BooleanField(default=False, help_text="0-show, 1-Hidden")  
    trending = models.BooleanField(default=False, help_text="0-default, 1-trending")  
    created_at = models.DateTimeField(auto_now_add=True)   
    updated_at = models.DateTimeField(auto_now=True)         

    def __str__(self):
        return self.name
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.quantity * self.product.selling_price

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"  

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()  # selling price at order time
    customer_name = models.CharField(max_length=20,blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})" 
