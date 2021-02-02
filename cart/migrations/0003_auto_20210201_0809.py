# Generated by Django 3.1.3 on 2021-01-31 23:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cart', '0002_auto_20201231_2319'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='buyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='buyer_in_cart_item', to=settings.AUTH_USER_MODEL, verbose_name='購入者'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='create_at',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='カート作成日時'),
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
    ]
