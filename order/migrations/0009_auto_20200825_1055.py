# Generated by Django 3.0.3 on 2020-08-25 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_order_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='納品完了フラグ'),
        ),
    ]
