from django.shortcuts import render, redirect, get_object_or_404
from item.models import Item
from .models import CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import math

__tax_rate__ = 1.1


@login_required
def add_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart_item, created = CartItem.objects.get_or_create(item=item, buyer=request.user, is_active=True)

    if item.stock > 0:
        try:
            if item.stock > cart_item.quantity:
                cart_item.quantity += 1
            cart_item.save()
        except Exception as e:
            print(e)
    else:
        pass

    return redirect('cart:cart_detail')


@login_required
def cart_detail(request, total=0, counter=0, cart_items=None,):
    warning_msg = {}
    try:
        cart_items = CartItem.objects.filter(buyer=request.user, is_active=True).order_by('-pk')
        error_msg = {}
        for cart_item in cart_items:
            if cart_item.item.stock > 0:
                if cart_item.item.stock > cart_item.quantity:
                    if cart_item.item.including_tax:
                        total += math.floor(cart_item.item.price * cart_item.quantity)
                        counter += cart_item.quantity
                    else:
                        total += math.floor(cart_item.item.price * cart_item.quantity * __tax_rate__)
                        counter += cart_item.quantity
                else:
                    if cart_item.item.including_tax:
                        total += math.floor(cart_item.item.price * cart_item.quantity)
                        warning_msg[cart_item.item_id] = 'こちらの商品は現在、在庫数が' + str(cart_item.item.stock) + cart_item.item.unit + 'です。'
                        cart_item.quantity = cart_item.item.stock
                        cart_item.save()
                    else:
                        total += math.floor(cart_item.item.price * cart_item.quantity * __tax_rate__)
                        warning_msg[cart_item.item_id] = 'こちらの商品は現在、在庫数が' + str(cart_item.item.stock) + cart_item.item.unit + 'です。'
                        cart_item.quantity = cart_item.item.stock
                        cart_item.save()
            else:
                total += math.floor(cart_item.item.price * cart_item.quantity * __tax_rate__)
                warning_msg[cart_item.item_id] = 'こちらの商品は現在、在庫がありません。'
                cart_item.quantity = 0
                cart_item.save()
    except ObjectDoesNotExist:
        pass
    return render(request, 'cart.html', dict(warning_msg=warning_msg, cart_items=cart_items, total=total))


@login_required
def reduce_quantity(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart_item = CartItem.objects.get(item=item, buyer=request.user, is_active=True)

    if item.stock >= cart_item.quantity:
        cart_item.quantity -= 1   # 数量を1減らす
        if cart_item.quantity < 1:
            cart_item.is_active = False
        cart_item.save()
    else:
        messages.error(request, 'こちらの商品は現在、在庫数が' + item.stock + 'です。')

    return redirect('cart:cart_detail')


@login_required
def cart_item_remove(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart_item = CartItem.objects.get(item=item, buyer=request.user, is_active=True)

    cart_item.is_active = False
    cart_item.save()

    return redirect('cart:cart_detail')
