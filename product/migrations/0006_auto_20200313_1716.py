# Generated by Django 3.0.4 on 2020-03-13 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_product_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='quantity',
        ),
        migrations.AddField(
            model_name='basketitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]