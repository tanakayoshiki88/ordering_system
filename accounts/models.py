from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime



class CustomUser(AbstractUser):
    '''拡張ユーザーモデル'''
    class Meta:
        app_label = 'accounts'
        db_table = 'custom_user'
        verbose_name_plural = 'CustomUser'

    postal_code = models.CharField(verbose_name='郵便番号', max_length=10, blank=True, null=True)
    state = models.CharField(verbose_name='都道府県', max_length=4, blank=True, null=True)
    city = models.CharField(verbose_name='区市町村名', max_length=7, blank=True, null=True)
    town = models.CharField(verbose_name='区域名番地等', max_length=20, blank=True, null=True)
    building = models.CharField(verbose_name='建物・部屋番号', max_length=20, blank=True, null=True)
    mobile = models.IntegerField(verbose_name='携帯番号', blank=True, null=True)
    phone = models.IntegerField(verbose_name='電話番号', blank=True, null=True)
    fax = models.IntegerField(verbose_name='Fax', blank=True, null=True)


    def get_full_name(self):
        """戻り地として last_name と first_name を間にスペースを挟んだ文字列 full_name を返すメソッド"""
        full_name = '%s %s' % (self.last_name, self.first_name)
        return full_name.strip()

    def __str__(self):
        return self.username
