# Generated by Django 5.0.6 on 2024-06-26 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0011_alter_image_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='po_number',
        ),
    ]
