# Generated by Django 3.1.3 on 2021-02-01 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_auto_20210131_2024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cart_id',
        ),
    ]
