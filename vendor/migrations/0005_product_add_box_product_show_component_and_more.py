# Generated by Django 5.0.6 on 2024-06-20 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0004_alter_order_order_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='add_box',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='show_component',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='track_qty',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='variable',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
    ]