# Generated by Django 5.0.6 on 2024-07-15 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0016_rename_comm_customer_check_dropship_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='bing',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='binmr',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='binother',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='binrr',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
    ]
