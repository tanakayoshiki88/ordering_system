from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('index/', views.IndexView.as_view(), name="index"),
    path('contact/', views.ContactView.as_view(), name="contact"),
    path('item-list/', views.ItemListView.as_view(), name="item_list"),
    path('item-create/', views.ItemCreateView.as_view(), name="item_create"),
    path('item-detail/<int:pk>/', views.ItemDetailView.as_view(), name="item_detail"),
    path('item-update/<int:pk>/', views.ItemUpdateView.as_view(), name="item_update"),
]
