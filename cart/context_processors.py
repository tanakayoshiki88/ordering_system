from .models import CartItem


def item_counter(request):
    number_of_items = 0

    if request.user.is_authenticated:
        try:
            cart_items = CartItem.objects.all().filter(buyer=request.user, is_active=True)
            for cart_item in cart_items:
                number_of_items += cart_item.quantity
        except Cart.DoesNotExist:
            number_of_items = 0
    else:
        pass
    return dict(number_of_items=number_of_items)
