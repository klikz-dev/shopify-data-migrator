# Generated by Django 5.0.6 on 2024-06-20 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0005_product_add_box_product_show_component_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='setpart',
            name='assoc',
        ),
        migrations.RemoveField(
            model_name='setpart',
            name='circulation',
        ),
        migrations.RemoveField(
            model_name='setpart',
            name='country',
        ),
        migrations.RemoveField(
            model_name='setpart',
            name='diameter',
        ),
        migrations.RemoveField(
            model_name='setpart',
            name='info',
        ),
        migrations.RemoveField(
            model_name='setpart',
            name='metal',
        ),
        migrations.RemoveField(
            model_name='setpart',
            name='obverse_detail',
        ),
        migrations.RemoveField(
            model_name='setpart',
            name='price',
        ),
        migrations.RemoveField(
            model_name='setpart',
            name='reverse_detail',
        ),
        migrations.RemoveField(
            model_name='setpart',
            name='unit_weight',
        ),
        migrations.AddField(
            model_name='product',
            name='variant_id',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
    ]
