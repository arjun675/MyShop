# Generated by Django 4.1.2 on 2022-11-28 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_alter_seller_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='pic',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
