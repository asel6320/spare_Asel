# Generated by Django 5.0.6 on 2024-10-13 14:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_alter_cart_part'),
        ('orders', '0002_alter_orderpart_part'),
        ('part', '0001_initial'),
        ('webapp', '0019_remove_orderpart_order_remove_orderpart_part_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricehistory',
            name='part',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_history', to='part.part'),
        ),
        migrations.AlterField(
            model_name='review',
            name='part',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='part.part', verbose_name='Запчасть'),
        ),
        migrations.DeleteModel(
            name='Part',
        ),
    ]