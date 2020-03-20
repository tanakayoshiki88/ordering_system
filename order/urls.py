from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('index/', views.IndexView.as_view(), name="index"),
    path('', views.IndexView.as_view(), name="index"),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('item-list/', views.ItemListView, name='item_list'),
    path('item-create/', views.ItemCreateView.as_view(), name='item_create'),
]
