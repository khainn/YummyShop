from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from category.models import Category
from carts.models import Cart, CartItem
from carts.views import _cart_id
from orders.models import OrderProduct
from store.models import Product, Event, Variation



def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)    # Get object product
    if current_user.is_authenticated:
        product_variations = list()
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST.get(key)
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variations.append(variation)
                except ObjectDoesNotExist:
                    pass

        is_exists_cart_item = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_exists_cart_item:
            cart_items = CartItem.objects.filter(
                product=product,
                user=current_user
            )
            existing_variation_list = [list(item.variations.all()) for item in cart_items]
            id = [item.id for item in cart_items]
            if product_variations in existing_variation_list:
                idex = existing_variation_list.index(product_variations)
                cart_item = CartItem.objects.get(id=id[idex])
                cart_item.quantity += 1
            else:
                cart_item = CartItem.objects.create(
                    product=product,
                    user=current_user,
                    quantity=1
                )
        else:
            cart_item = CartItem.objects.create(
                product=product,
                user=current_user,
                quantity=1
            )
        if len(product_variations) > 0:
            cart_item.variations.clear()
            for item in product_variations:
                cart_item.variations.add(item)
        cart_item.save()
        return redirect('cart')
    else:
        product_variations = list()
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST.get(key)
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variations.append(variation)
                except ObjectDoesNotExist:
                    pass
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request=request))  # Get cart using the _cart_id
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()

        is_exists_cart_item = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_exists_cart_item:
            cart_items = CartItem.objects.filter(
                product=product,
                cart=cart
            )
            existing_variation_list = [list(item.variations.all()) for item in cart_items]
            id = [item.id for item in cart_items]
            if product_variations in existing_variation_list:
                idex = existing_variation_list.index(product_variations)
                cart_item = CartItem.objects.get(id=id[idex])
                cart_item.quantity += 1
            else:
                cart_item = CartItem.objects.create(
                    product=product,
                    cart=cart,
                    quantity=1
                )
        else:
            cart_item = CartItem.objects.create(
                product=product,
                cart=cart,
                quantity=1
            )
        if len(product_variations) > 0:
            cart_item.variations.clear()
            for item in product_variations:
                cart_item.variations.add(item)
        cart_item.save()
        return redirect('cart')