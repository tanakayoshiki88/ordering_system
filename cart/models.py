from django.db import models
from item.models import Item
from accounts.models import CustomUser
from django.utils import timezone
from django.urls import reverse


class CartItem(models.Model):
    """カートアイテムモデル"""
    class Meta:
        # アプリケーション名
        app_label = 'cart'
        # テーブル名
        db_table = 'cart_item'
        # django 管理画面の表示、名前末尾に s は表示されない
        verbose_name_plural = 'カートアイテム'

    item = models.ForeignKey(Item, verbose_name='商品', on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='数量', default=0)
    is_active = models.BooleanField(default=True)
    buyer = models.ForeignKey(
        CustomUser,
        verbose_name='購入者',
        on_delete=models.PROTECT,
        related_name='buyer_in_cart_item',
        blank=True,
        null=True
    )
    create_at = models.DateTimeField(verbose_name='カート作成日時', default=timezone.now)

    def sub_total(self):
        return self.item.price * self.quantity

    def __str__(self):
        return str(self.item.id)

    def get_absolute_url(self):
        return reverse("item:item_detail", kwargs={'pk': self.item.pk})
