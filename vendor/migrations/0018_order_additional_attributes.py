# Generated by Django 5.0.6 on 2024-07-16 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0017_alter_product_bing_alter_product_binmr_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='additional_attributes',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
