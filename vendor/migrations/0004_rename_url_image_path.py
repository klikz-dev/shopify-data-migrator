# Generated by Django 5.0.6 on 2024-05-30 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0003_collection_parents'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='url',
            new_name='path',
        ),
    ]