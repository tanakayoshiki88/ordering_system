# Generated by Django 3.1.3 on 2020-12-31 14:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0005_auto_20201201_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='作成日時'),
        ),
    ]