# Generated by Django 5.0.6 on 2024-06-12 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0014_setpart_parent_order_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='setpart',
            name='info',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
    ]