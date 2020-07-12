from accounts.models import CustomUser
from django.db import models
from datetime import datetime
from item.models import Item


class Order(models.Model):
    '''注文モデル'''
    class Meta:

        # テーブル名
        db_table = 'order'
        # django 管理画面の表示、名前末尾に s は表示されない
        verbose_name_plural = '注文明細'

    # カラム定義
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)
    item = models.ForeignKey(Item, verbose_name='商品', on_delete=models.PROTECT)
    quantity = models.IntegerField(verbose_name='数量')
    total_price = models.IntegerField(verbose_name='合計金額', default=0)
    order_date = models.DateTimeField(verbose_name='注文日', default=datetime.now)
    delivery_date = models.DateTimeField(verbose_name='納品日', blank=True, null=True)
    shipment_date = models.DateTimeField(verbose_name='発送日', blank=True, null=True)
    is_cancel = models.BooleanField(verbose_name='キャンセル', default=False)
    remarks = models.TextField(verbose_name='備考', max_length=150, blank=True, null=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)
