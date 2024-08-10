from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField( auto_now=True, auto_now_add=False)
    phone = models.CharField(max_length=10, blank=True)
    address1 = models.CharField(max_length=100, blank=True)
    address2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=502, blank=True)
    state = models.CharField(max_length=503, blank=True)
    zipcode = models.CharField(max_length=140, blank=True)
    contry = models.CharField( max_length=250, blank=True)
    old_cart = models.CharField(max_length=250, blank=True)
    

    def __str__(self):
        return self.user.username
    
   # create a user profil by default when user signs up  
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        
        
#automate the profilr things        
post_save.connect(create_profile, sender=User)
        
        
        
        




class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'categories'
    


class customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone =  models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name
    


class Product(models.Model):
    name =models.CharField(max_length=50)
    price =models.DecimalField(default=0,decimal_places=2,max_digits=7)
    category =models.ForeignKey(Category,on_delete=models.CASCADE, default=1)
    description =models.CharField(max_length=150,default='', blank=True, null=True)
    image =models.ImageField(upload_to='upload/product/')
    is_sale =models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0,decimal_places=2,max_digits=7)


    def __str__(self):
        return self.name
    



class order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='',blank=True)
    phone = models.CharField(max_length=20, default='',blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product
    
    
    
