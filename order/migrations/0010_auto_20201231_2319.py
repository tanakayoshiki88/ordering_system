# Generated by Django 3.1.3 on 2020-12-31 14:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_auto_20200825_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='注文日'),
        ),
    ]
