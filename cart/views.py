from django.shortcuts import render, redirect, get_object_or_404
from item.models import Item
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

import math

__tax_rate__ = 1.1

"""セッションキー取得機能"""
def __get_cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id

@login_required
def add_cart(request, item_id):
    item = Item.objects.get(id=item_id)
    try:
        cart = Cart.objects.get(cart_id=__get_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
                cart_id=__get_cart_id(request)
            )
        cart.save()
    try:
        cart_item = CartItem.objects.get(item=item, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
                item=item,
                quantity=1,
                cart=cart
            )
        cart_item.save()
    return redirect('cart:cart_detail')

@login_required
def cart_detail(request, total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=__get_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True).order_by('-pk')
        for cart_item in cart_items:
            if cart_item.item.including_tax:
                total += math.floor(cart_item.item.price * cart_item.quantity)
                counter += cart_item.quantity
            else:
                total += math.floor(cart_item.item.price * cart_item.quantity * __tax_rate__)
                counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request, 'cart.html', dict(cart_items=cart_items, total=total, counter=counter))

@login_required
def reduce_quantity(request, item_id):
    cart = Cart.objects.get(cart_id=__get_cart_id(request))
    item = get_object_or_404(Item, id=item_id)
    cart_item = CartItem.objects.get(item=item, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')

@login_required
def cart_item_remove(request, item_id):
    cart = Cart.objects.get(cart_id=__get_cart_id(request))
    item = get_object_or_404(Item, id=item_id)
    cart_item = CartItem.objects.get(item=item, cart=cart)
    cart_item.delete()
    return redirect('cart:cart_detail')
