# Generated by Django 3.0.3 on 2020-07-29 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0002_auto_20200725_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=40, verbose_name='商品名'),
        ),
    ]
