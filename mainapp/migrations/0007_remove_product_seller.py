# Generated by Django 4.1.2 on 2022-12-07 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_product_seller_alter_seller_pin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='seller',
        ),
    ]
