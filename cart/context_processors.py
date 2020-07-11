from .models import Cart, CartItem
from .views import get_cart_id


def item_counter(request):
    number_of_items = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=get_cart_id(request))
            cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                number_of_items += cart_item.quantity
        except Cart.DoesNotExist:
            number_of_items = 0
    return dict(number_of_items=number_of_items)
