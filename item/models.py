from accounts.models import CustomUser
from django.db import models
from datetime import datetime
from django.urls import reverse


class Item(models.Model):
    '''商品モデル'''
    class Meta:
        app_label = 'item'
        # テーブル名
        db_table = 'item'
        # django 管理画面の表示、名前末尾に s は表示されない
        verbose_name_plural = '商品'

    # カラム定義
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)
    name = models.CharField(verbose_name='商品名', max_length=40, unique=True)
    price = models.IntegerField(verbose_name='単価', default=0)
    including_tax = models.BooleanField(verbose_name='税込', default=False)
    unit = models.CharField(verbose_name='単位', max_length=10, default='個')
    stock = models.IntegerField(verbose_name='在庫数', blank=True, null=True)
    moq = models.IntegerField(verbose_name='最低発注数量', blank=True, null=True, default=0)
    spq = models.IntegerField(verbose_name='最小発注単位', blank=True, null=True, default=0)
    category1 = models.CharField(verbose_name='カテゴリ1', max_length=30, blank=True, null=True)
    category2 = models.CharField(verbose_name='カテゴリ2', max_length=30, blank=True, null=True)
    category3 = models.CharField(verbose_name='カテゴリ3', max_length=30, blank=True, null=True)
    photo = models.ImageField(verbose_name='商品画像', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='作成日時', default=datetime.now)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    is_active = models.BooleanField(verbose_name='販売可否', default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("item:item_list")

