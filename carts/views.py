from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product
from .models import Cart,CartItem
# Create your views here.


from django.http import HttpResponse


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    
    # Check if user is logged in
    if request.user.is_authenticated:
        # 1. Look for the item specifically for THIS user
        try:
            cart_item = CartItem.objects.get(product=product, user=request.user)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            # 2. If it doesn't exist, create it linked to the user
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=request.user,
                # We can leave 'cart' as None if your model allows null=True
            )
        return redirect('cart')
    
    else:
        # If not logged in, you can either redirect to login 
        # or keep the session logic as a fallback.
        return redirect('login')
    
from django.core.exceptions import ObjectDoesNotExist

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            # Fetch items linked to the logged-in user
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            # Fallback or empty list for guests
            cart_items = []

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            
    except ObjectDoesNotExist:
        pass # Just render an empty cart

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
    }
    return render(request, 'store/cart.html', context)


from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        # Fetching items for the logged-in user
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        
        tax = (2 * total) / 100
        grand_total = total + tax
        
    except ObjectDoesNotExist:
        pass # Just handle as empty

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)


def remove_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, user=request.user)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def delete_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, user=request.user)
    cart_item.delete()
    return redirect('cart')