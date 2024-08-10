from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem

admin.site.register(ShippingAddress)
# Register your models here.

admin.site.register(Order)

admin.site.register(OrderItem)