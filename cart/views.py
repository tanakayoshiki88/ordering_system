from django.shortcuts import render, redirect, get_object_or_404
from item.models import Item
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

import math

__tax_rate__ = 1.1

"""セッションキー取得機能"""
def __get_cart_id(request):

    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id


def add_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    try:
        if item.available_stock < 1:
            raise ValueError('有効在庫が 0 です。')
            messages.error(request, '在庫不足のためカートに商品を追加できませんでした。')

        item.available_stock -= 1
        item.reserved_stock += 1

        item.save()
    except ValueError as e:
        print(e)

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
    return render(request, 'cart.html', dict(cart_items=cart_items, total=total ))


def reduce_quantity(request, item_id):
    cart = Cart.objects.get(cart_id=__get_cart_id(request))
    item = get_object_or_404(Item, id=item_id)
    cart_item = CartItem.objects.get(item=item, cart=cart)

    if item.reserved_stock > 0:
        item.available_stock += 1  # 有効在庫数を1増やす
        item.reserved_stock -= 1   # 引当在庫数を1減らす
        item.save()
    else:
        messages.error(request, '数量が 0 です。数量を減らすことが出来ません。管理者に問合せてください。')
        return redirect('cart:cart_detail')

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')


def cart_item_remove(request, item_id):
    cart = Cart.objects.get(cart_id=__get_cart_id(request))
    item = get_object_or_404(Item, id=item_id)
    cart_item = CartItem.objects.get(item=item, cart=cart)

    if item.reserved_stock > 0:
        item.available_stock += 1  # 有効在庫数を1増やす
        item.reserved_stock -= 1   # 引当在庫数を1減らす
        item.save()
    else:
        messages.error(request, '数量が 0 です。数量を減らすことが出来ません。管理者に問合せてください。')
        return redirect('cart:cart_detail')

    cart_item.delete()
    return redirect('cart:cart_detail')
