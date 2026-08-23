from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from .models import Product, Category, CartItem


# This view returns the 'storehome.html' file.
def storehome(request):
    return render(request, 'store/storehome.html', {})


# This view returns the 'store/aboutus.html' file.
def aboutus(request):
    return render(request, 'store/aboutus.html', {'title': 'About Us'})


# This view returns the 'store/reviews.html' file.
def reviews(request):
    return render(request, 'store/reviews.html', {'title': 'Reviews'})

# The Updated version in chapter 6 -  This view returns the 'store/shop.html' file.
def shop(request, category = None):
    if category:
        category = Category.objects.get(name=category)
        products = Product.objects.filter(category=category)
        return render(request, 'store/shop.html', {'products': products, 'category' : category, 'title': category})
    else:
        products = Product.objects.all()
        return render(request, 'store/shop.html', {'products': products, 'title': 'All Phones' })


def product(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'store/product.html', {'product' : product, 'title': product.name })


def add_to_cart(request, product_id):
    if request.user :
       product = Product.objects.get(id=product_id)
       cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
       cart_item.quantity += 1
       cart_item.save()
       return redirect('shop')

from django.contrib.auth.decorators import login_required


@login_required(login_url='login_user')
def view_cart(request):
    if request.user.is_anonymous:
        pass
    else:
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.sale_price * item.quantity for item in cart_items)
        return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price, 'title': 'Shopping Cart'})

def cart_items_context(request):
    cart_items_count = CartItem.objects.filter(user=request.user).count()
    return {'cart_items_count': cart_items_count}

@login_required(login_url='login_user')
def remove_from_cart(request, item_id):
    """Remove an item from the cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    
    messages.success(request, f'{product_name} removed from cart.')
    return redirect('view_cart')