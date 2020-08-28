# Generated by Django 3.0.3 on 2020-07-02 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.IntegerField(default=0, verbose_name='合計金額'),
        ),
        migrations.RemoveField(
            model_name='order',
            name='quantity',
        ),
    ]