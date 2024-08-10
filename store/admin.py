from django.contrib import admin
from .models import Category,customer,Product,order, Profile
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Category)
admin.site.register(customer)
admin.site.register(Product)
admin.site.register(order)
admin.site.register(Profile)

# mix profile info and user info
class ProfileInline(admin.StackedInline):
    model = Profile
    
 # Extend user model   
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]
# unregister the old way
admin.site.unregister(User)

# re-Register in the new way
admin.site.register(User, UserAdmin)

