from django.db import models

# Create your models here. 
class Contact_Db(models.Model):
    First_name=models.CharField(max_length=200, null=True,blank=True)
    Last_name=models.CharField(max_length=200, null=True,blank=True)
    Email =models.EmailField(max_length=200, null=True,blank=True)
    Message=models.TextField(max_length=200, null=True,blank=True)

class SignUp_Db(models.Model):
    Name=models.CharField(max_length=200, null=True,blank=True)
    Mobile_number=models.IntegerField(null=True,blank=True)
    Email =models.EmailField(max_length=200, null=True,blank=True)
    Password=models.CharField(max_length=200, null=True,blank=True)
    Repeat_Password=models.CharField(max_length=200, null=True,blank=True)

class Cart_Db(models.Model):
    User_name=models.CharField(max_length=200, null=True,blank=True)
    Product_name=models.CharField(max_length=200, null=True,blank=True)
    Quantity=models.CharField(max_length=200, null=True,blank=True)
    Price=models.FloatField(null=True,blank=True)
    Total_Price=models.FloatField(null=True,blank=True)
    product_image=models.ImageField(upload_to="cart_images",null=True,blank=True)

class Order_Db(models.Model):
    Name=models.CharField(max_length=200, null=True,blank=True)
    Email=models.EmailField(max_length=200, null=True,blank=True)
    Phone=models.IntegerField(null=True,blank=True)
    Place=models.CharField(max_length=200, null=True,blank=True)
    total=models.FloatField(null=True,blank=True)
    Address=models.CharField(max_length=200,null=True,blank=True)
    Message=models.TextField(max_length=200,null=True,blank=True)


   
    

