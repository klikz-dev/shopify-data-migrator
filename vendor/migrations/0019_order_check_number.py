# Generated by Django 5.0.6 on 2024-07-16 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0018_order_additional_attributes'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='check_number',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
    ]
