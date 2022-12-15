from django.shortcuts import render
from store.models import Product, Event
from category.models import Category
from django.core.paginator import Paginator
from carts.models import Cart, CartItem
from carts.views import _cart_id
from orders.models import OrderProduct
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status

def home(request):
    products = Product.objects.all().filter(is_available=True)
    categoris = Category.objects.all()
    events = Event.objects.all()

    try:   
        cart = Cart.objects.get(cart_id=_cart_id(request=request))
        in_cart = CartItem.objects.filter(
            cart=cart,
        ).exists()
    except Exception as e:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )


    context = {
        'in_cart': in_cart if 'in_cart' in locals() else False,
        'products': products,
        'categoris' : categoris,
        'events': events
    }
    return render(request, 'home.html', context=context)

def add_cart(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if(is_ajax and request.method == "POST"):
        current_user = request.user
        product_id = request.GET['product_id']
        product = Product.objects.get(id=product_id)    # Get object product
        if current_user.is_authenticated:
            is_exists_cart_item = CartItem.objects.filter(product=product, user=current_user).exists()
        
        if is_exists_cart_item:           
            cart_item = CartItem.objects.get(
                product=product,
                user=current_user
            )
            cart_item.quantity += 1
        else:
            cart_item = CartItem.objects.create(
                    product=product,
                    user=current_user,
                    quantity=1
                )
        cart_item.save()
    return JsonResponse({'message': 'Update Cart unsuccessful!'}, status.HTTP_200_OK)
    
