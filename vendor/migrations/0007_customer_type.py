# Generated by Django 5.0.6 on 2024-06-21 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0006_remove_setpart_assoc_remove_setpart_circulation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='type',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
    ]
