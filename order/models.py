from accounts.models import CustomUser
from django.db import models
from django.utils import timezone


class Order(models.Model):
    """注文モデル"""
    class Meta:
        app_label = 'order'
        # テーブル名
        db_table = 'order'
        # django 管理画面の表示、名前末尾に s は表示されない
        verbose_name_plural = '注文明細'
        ordering = ['-order_date']

    # カラム定義
    buyer = models.ForeignKey(CustomUser, verbose_name='購入者', on_delete=models.PROTECT, related_name='buyer_in_order')
    seller = models.ForeignKey(CustomUser, verbose_name='販売者', on_delete=models.PROTECT, related_name='seller')
    item_id = models.CharField(verbose_name='商品ID', max_length=40, default='dummy_item_id')
    name = models.CharField(verbose_name='商品名', max_length=40, default='dummy_name')
    price = models.IntegerField(verbose_name='単価', default=0)
    including_tax = models.BooleanField(verbose_name='税込', default=False)
    quantity = models.IntegerField(verbose_name='数量', default=0)
    unit = models.CharField(verbose_name='単位', max_length=10, default='個')
    moq = models.IntegerField(verbose_name='最低発注数量', blank=True, null=True, default=0)
    spq = models.IntegerField(verbose_name='最小発注単位', blank=True, null=True, default=0)
    photo = models.ImageField(verbose_name='商品画像', blank=True, null=True)
    total_unit = models.IntegerField(verbose_name='商品点数', default=0)
    total_price = models.IntegerField(verbose_name='合計金額', default=0)
    order_date = models.DateTimeField(verbose_name='注文日', default=timezone.now)
    delivery_date = models.DateTimeField(verbose_name='納品日', blank=True, null=True)
    shipment_date = models.DateTimeField(verbose_name='発送日', blank=True, null=True)
    is_active = models.BooleanField(verbose_name='納品完了フラグ', default=True)
    is_cancel = models.BooleanField(verbose_name='キャンセル', default=False)
    remarks = models.TextField(verbose_name='備考', max_length=150, blank=True, null=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)
