# Generated by Django 4.1.2 on 2022-12-27 21:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0013_wishlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wishlist',
            old_name='Product',
            new_name='product',
        ),
    ]
