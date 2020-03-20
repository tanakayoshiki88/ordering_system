# Generated by Django 3.0.3 on 2020-03-18 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='building',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='建物・部屋番号'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='city',
            field=models.CharField(blank=True, max_length=7, null=True, verbose_name='区市町村名'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='fax',
            field=models.IntegerField(blank=True, max_length=16, null=True, verbose_name='Fax'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='mobile',
            field=models.IntegerField(blank=True, max_length=11, null=True, verbose_name='携帯番号'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone',
            field=models.IntegerField(blank=True, max_length=10, null=True, verbose_name='電話番号'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='postal_code',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='郵便番号'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='state',
            field=models.CharField(blank=True, max_length=4, null=True, verbose_name='都道府県'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='town',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='区域名番地等'),
        ),
        migrations.AlterModelTable(
            name='customuser',
            table='custome_user',
        ),
    ]
