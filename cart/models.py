from django.db import models
from item.models import Item
from datetime import datetime
from django.urls import reverse


class Cart(models.Model):
    '''カートモデル'''
    class Meta:
        # アプリケーション名
        app_label = 'cart'
        # テーブル名
        db_table = 'cart'
        # django 管理画面の表示、名前末尾に s は表示されない
        verbose_name_plural = 'カート'
        # ソート順
        ordering = ['create_at']

    cart_id = models.CharField(verbose_name='カートID', max_length=250, blank=True)
    create_at = models.DateField(verbose_name='カート作成日時', default=datetime.now)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    '''カートアイテムモデル'''
    class Meta:
        # アプリケーション名
        app_label = 'cart'
        # テーブル名
        db_table = 'cart_item'
        # django 管理画面の表示、名前末尾に s は表示されない
        verbose_name_plural = 'カートアイテム'

    item = models.ForeignKey(Item, verbose_name='商品', on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, verbose_name='カート', on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='数量')
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.item.price * self.quantity

    def __str__(self):
        return self.item

    def get_absolute_url(self):
        return reverse("item:item_detail", kwargs={'pk': self.item.pk})
