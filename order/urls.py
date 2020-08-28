from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('index/', views.IndexView.as_view(), name="index"),
    path('contact/', views.ContactView.as_view(), name="contact"),
    path('order-create/', views.order_create, name='order_create'),
    path('placed-order-list/', views.PlacedOrderListView.as_view(), name="placed_order_list"),
    path('received-order-list/', views.received_order_list, name="received_order_list"),
#    path('order/favorite-item-create/<int:pk>/<str:name>/', views.FavoriteItemCreateView.as_view(), name="favorite_item_create"),
]
