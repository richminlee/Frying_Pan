# Generated by Django 3.2.4 on 2021-08-20 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frypan', '0005_rename_full_price_item_discount_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='img',
            field=models.CharField(default='https://mdbootstrap.com/img/Photos/Horizontal/E-commerce/Vertical/12.jpg', max_length=500),
            preserve_default=False,
        ),
    ]