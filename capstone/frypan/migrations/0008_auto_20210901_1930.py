# Generated by Django 3.2.4 on 2021-09-02 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frypan', '0007_rename_category_item_label_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='label_color',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
