# Generated by Django 3.0.3 on 2020-03-18 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200318_1333'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='customuser',
            table='custom_user',
        ),
    ]