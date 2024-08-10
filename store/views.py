from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate,login ,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# .forms is a file name that are module 
#this signup is inheret/import to class SignUPpFomr in form.py file se
from .forms import SignUpForm,UpdateUserForm, ChangePasswordForm, UserInfoFrom


from payment.forms import ShippingForm
from payment.models import ShippingAddress

from django import forms
from django.db.models import Q
import json
from cart.cart import Cart

from django.core.exceptions import ObjectDoesNotExist

'''
def update_info(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        try:
            # Get the current user
            current_user = Profile.objects.get(user__id=request.user.id)
            
            # Get the current user's shipping info (assuming there's a foreign key reference)
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        except (Profile.DoesNotExist, ShippingAddress.DoesNotExist):
            messages.error(request, "Profile or shipping address does not exist for the current user.")
            return redirect("home")

        # Initialize forms
        form = UserInfoFrom(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        # Check if both forms are valid
        if form.is_valid() and shipping_form.is_valid():
            # Save the forms
            form.save()
            shipping_form.save()
            # Display a success message
            messages.success(request, "Your info has been updated.")
            # Redirect to the home page
            return redirect("home")

        # Render the update_info.html template with the forms
        return render(request, 'update_info.html', {'form': form, 'shipping_form': shipping_form})  # Pass shipping_form to the template
    else:
        # Display an error message if the user is not authenticated
        messages.error(request, "You must be logged in to access that page.")
        # Redirect to the home page
        return redirect("home")

'''
def update_info(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        try:
            # Get the current user
            current_user = Profile.objects.get(user__id=request.user.id)
            
            # Get the current user's shipping info (assuming there's a foreign key reference)
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        except (Profile.DoesNotExist, ShippingAddress.DoesNotExist):
            messages.error(request, "Profile or shipping address does not exist for the current user.")
            return redirect("home")

        # Initialize forms
        form = UserInfoFrom(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        # Check if both forms are valid
        if form.is_valid() and shipping_form.is_valid():
            # Save the forms
            form.save()
            shipping_form.save()
            # Display a success message
            messages.success(request, "Your info has been updated.")
            # Redirect to the home page
            return redirect("home")

        # Render the update_info.html template with the forms
        return render(request, 'update_info.html', {'form': form, 'shipping_form': shipping_form})
    else:
        # Display an error message if the user is not authenticated
        messages.error(request, "You must be logged in to access that page.")
        # Redirect to the home page
        return redirect("home")


def search(request):
    if request.method == "POST":
        searched = request.POST.get('searched', '')  # Using get() method to avoid MultiValueDictKeyError
        # search for products (query the product DB model)that machines the  search and return results from the search method if available and return 
        # icontains is case insensitive (P=p)and returns only products that  match   the search  criteria    
        
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        
        if not searched:
            messages.success(request, "Product does not exist...", "product")
            
       
       
        return render(request, 'search.html', {'searched': searched})
    else:
        return render(request, 'search.html', {})


    


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            #it the form valid
            if form.is_valid():
                form.save()
                messages.success(request, "you password is update , please Login In  Again")
                return redirect("login")
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect("update_password")
                
            
            #get the password for the form
           #password = request.POST['password']
          # foo = current_user 
        
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html",{'form':form})
            
    else:
        messages.success(request, "You Must Be Logged In To Access That Page")
        return redirect("home")
    
    
    
    return render(request, 'update_password.html',{})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            
            login(request, current_user)
            messages.success(request, "user has Been Updated")
            return redirect("home")
        
        
        return render(request, 'update_user.html', {'user_form':user_form})
    else:
        messages.success(request, "You Must Be Logged In To Access That Page")
        return redirect("home")
def category(request, foo):
    #Replace Hyphens with spaces
    foo = foo.replace('-', ' ')
    # grap the categary from the url
    try:
        #look up the category
        category = Category.objects.get(name=foo)
        #in product model we  filer the category and send it argument to the function
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})




    except:
            messages.success(request, "That category Doesn't Exist...")
            return redirect('home')

def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})



# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
    return render(request, 'about.html', {})
    
'''
def login_user(request):
    if request.method == 'POST':
        
        username1 = request.POST['username']
        password1 = request.POST['password']
        user = authenticate( username=username1, password=password1)
        if user is not None:
    
            login(request, user)
            
            # do same shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            
            saved_cart = current_user.old_cart
            
            if saved_cart:
                #converted to dictionary using JSON
                coverted_cart = json.loads(saved_cart)
                #Add the loaded cart dictionary to our session
                #get the cart 
                cart = Cart(request)
                #loop through the dictionary and add the items to the cart
                for key, value in coverted_cart.items():
                    cart.db_add(product=key, quantity=value)
    
    
    
    
    
            messages.success(request, ("you have been login success"))
            return redirect('home')
        else:
            messages.success(request, ("there was same error.. pleace try again"))
        return redirect('login')
    else:
        return render(request, 'login.html', {})
    '''



def login_user(request):
    if request.method == 'POST':
        username1 = request.POST['username']
        password1 = request.POST['password']
        user = authenticate(username=username1, password=password1)
        if user is not None:
            login(request, user)
            try:
                current_user_profile = Profile.objects.get(user=user)
                saved_cart = current_user_profile.old_cart
                if saved_cart:
                    # Convert the saved cart to dictionary using JSON
                    converted_cart = json.loads(saved_cart)
                    # Add the loaded cart dictionary to our session
                    cart = Cart(request)
                    # Loop through the dictionary and add the items to the cart
                    for key, value in converted_cart.items():
                        cart.db_add(product=key, quantity=value)
            except ObjectDoesNotExist:
                # Handle the case where the profile doesn't exist
                messages.error(request, "Profile matching query does not exist.")
                return redirect('home')
            messages.success(request, "You have been logged in successfully!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('login')
    else:
        return render(request, 'login.html', {})

    
    
def logout_user(request):
    logout(request)
    messages.success(request, ("you have been lagout out....."))
    return redirect('login')


def register_user(request):
    form = SignUpForm()
    #post must capital 
    
    if request.method == "POST":
        form = SignUpForm(request.POST)
        #if form is valid then save 
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("you have registered Successfully!! welcome"))
            return redirect('update_info')
        
        else:
            messages.success(request, ("oooops.. there is same problem"))
            return redirect('register')

    else:
        return render(request, 'register.html', {'form':form})