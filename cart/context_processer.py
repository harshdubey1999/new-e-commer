from .cart import Cart 

#create context processor so our cart can work on all page 
def cart(request):
    #return the default datafrom our Cart
    return {'cart': Cart(request)}