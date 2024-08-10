from django.shortcuts import render

# Create your views here.
from . import views

def payment_success(request):

    return render(request, "payment/payment_success.html")