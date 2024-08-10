from django.db import models
from django.contrib.auth.models import User
#from django.db.models.signals import post_save
from store.models import Product


# Create your models here.
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=50)
    shipping_email = models.EmailField(max_length=254)
    shipping_address1 = models.CharField(max_length=50)
    shipping_address2 = models.CharField(max_length=50)
    shipping_city = models.CharField( max_length=50)
    shipping_state = models.CharField(max_length=50)
    shipping_zipcode = models.CharField(max_length=50)
    shipping_country = models.CharField(max_length=50)
    
    class Meta:
        verbose_name_plural = 'Shipping Addresses'
    def __str__(self):
        return f'Shipping Address - {str(self.id)}'

# Create orde  model 

class Order(models.Model):
    #Foreign key
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=254)
    shipping_address = models.TextField(max_length=150000)
    amount_paid = models.DecimalField(max_digits=15, decimal_places=2)
    date_ordered = models.DateField( auto_now_add=True)
    
    def __str__(self):
        return f'Order - {str(self.id)}'
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    
    def __str__(self):
        return f'Order Item - {str(self.id)}'