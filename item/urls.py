from django.urls import path
from . import views

app_name = 'item'

urlpatterns = [
    path('item-list/', views.ItemListView.as_view(), name="item_list"),
    path('item-create/', views.ItemCreateView.as_view(), name="item_create"),
    path('item-detail/<int:pk>/', views.ItemDetailView.as_view(), name="item_detail"),
    path('item-update/<int:pk>/', views.ItemUpdateView.as_view(), name="item_update"),
    path('item-delete/<int:pk>/', views.ItemDeleteView.as_view(), name="item_delete"),
    path('order-item-list/', views.OrderItemListView.as_view(), name="order_item_list"),
    path('search-item-list/', views.SearchItemListView.as_view(), name="search_item_list"),
]
