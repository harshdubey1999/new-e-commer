from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

# Create your views here.
def cart_summary(request):
        
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        return render(request, "cart_summary.html",{'cart_products': cart_products, "quantities": quantities, "totals":totals})
    
    
def cart_add(request):
        #get the cart
        cart = Cart(request)
        #test the POST (POST for button and "post" action
        if request.POST.get('action') == 'post':
                #get the product
                product_id = int(request.POST.get('product_id'))
                # lookup product in database
                product_qty = int(request.POST.get('product_qty'))
                
                product = get_object_or_404(Product, id=product_id)
               # save to session
                cart.add(product=product, quantity=product_qty )
                
                
                #get cart quantity
                cart_quantity = cart.__len__()
                
                
                #response = JsonResponse({'Product Name: ': product.id})
                response = JsonResponse({'qty': cart_quantity})
                return response
               
def cart_delete(request):
        
        cart = Cart(request)
        #test the POST (POST for button and "post"  for action
        if request.POST.get('action') == 'post':
                product_id = int(request.POST.get('product_id'))
                cart.delete(product=product_id)
                            
                response = JsonResponse({'product':product_id})
                return response
               

def cart_update(request):
        
        cart = Cart(request)
        #test the POST (POST for button and "post"  for action
        if request.POST.get('action') == 'post':
                #get the product
                product_id = int(request.POST.get('product_id'))
                # lookup product in database
                product_qty = int(request.POST.get('product_qty'))
                
                cart.update(product=product_id, quantity=product_qty)
                
                response = JsonResponse({'qty':product_qty})
                return response
                
        
        
               # return render(request, 'cart_summaty.html')


         