# Generated by Django 5.0.6 on 2024-06-05 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0008_product_product_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='circulation',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='custom_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='era',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='height',
            field=models.FloatField(blank=True, default=1, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='length',
            field=models.FloatField(blank=True, default=1, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='msrp',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='news_from_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='news_to_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='obverse_detail',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='parent_sku',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='product_attachment_file',
            field=models.CharField(blank=True, default=None, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='region',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='reverse_detail',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
    ]
