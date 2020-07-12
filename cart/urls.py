from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add-cart/<int:item_id>/', views.add_cart, name='add_cart'),
    path('', views.cart_detail, name='cart_detail'),
    path('reduce-quantity/<int:item_id>/', views.reduce_quantity, name='reduce_quantity'),
    path('cart-item-remove/<int:item_id>/', views.cart_item_remove, name='cart_item_remove'),
]


