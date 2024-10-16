# Generated by Django 5.0.6 on 2024-10-16 07:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_no', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('email', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('phone', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('first_name', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('last_name', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('company', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('address1', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('address2', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('city', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('state', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('zip', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('country', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('note', models.TextField(blank=True, default=None, max_length=2000, null=True)),
                ('tags', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('customer_type', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('trade_show_sales_representative', models.BooleanField(default=False)),
                ('payment_terms', models.IntegerField(blank=True, default=None, null=True)),
                ('vat_no', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('orig_ad', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('check_dropship', models.BooleanField(default=False)),
                ('additional_attributes', models.JSONField(blank=True, default=dict, null=True)),
                ('customer_id', models.CharField(blank=True, default=None, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Setpart',
            fields=[
                ('order_code', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('parent_order_code', models.CharField(blank=True, default=None, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('parents', models.ManyToManyField(blank=True, related_name='subcollections', to='vendor.collection')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('company_name', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('company_note', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('location_name', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('location_note', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('location_phone', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('location_tax_exemption', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('shipping_first_name', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('shipping_last_name', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('shipping_phone', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('shipping_address1', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('shipping_address2', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('shipping_city', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('shipping_state', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('shipping_zip', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('shipping_country', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('billing_first_name', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('billing_last_name', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('billing_phone', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('billing_address1', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('billing_address2', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('billing_city', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('billing_state', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('billing_zip', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('billing_country', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('company_id', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='companies', to='vendor.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_no', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('order_total', models.FloatField(default=0)),
                ('order_date', models.DateField(blank=True, null=True)),
                ('terms', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('terms_due_date', models.DateField(blank=True, null=True)),
                ('order_code', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('discount', models.FloatField(default=0)),
                ('payment_method', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('card_type', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('approval', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('shipping_method', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('shipping_cost', models.FloatField(default=0)),
                ('order_memo', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('customer_no', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('company', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('amount_paid', models.FloatField(default=0)),
                ('po_number', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('tracking_number', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('sales_rep_robin', models.BooleanField(default=False)),
                ('check_number', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('checkamoun', models.FloatField(blank=True, default=0, null=True)),
                ('credit_memo', models.FloatField(blank=True, default=0, null=True)),
                ('additional_attributes', models.JSONField(blank=True, default=dict, null=True)),
                ('order_id', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='vendor.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('sku', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('handle', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('description', models.TextField(blank=True, default=None, max_length=5000, null=True)),
                ('barcode', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('wholesale', models.FloatField(default=0)),
                ('retail', models.FloatField(blank=True, default=0, null=True)),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('weight', models.FloatField(blank=True, default=1, null=True)),
                ('status', models.BooleanField(default=True)),
                ('add_box', models.BooleanField(default=True)),
                ('show_component', models.BooleanField(default=True)),
                ('track_qty', models.BooleanField(default=True)),
                ('parent_sku', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('length', models.FloatField(blank=True, default=1, null=True)),
                ('height', models.FloatField(blank=True, default=1, null=True)),
                ('country', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('order_code', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('dimensions', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('denomination', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('era', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('metal', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('misc_product_info', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('obverse_detail', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('region', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('reverse_detail', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('ruler', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('size', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('subcategory', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('custom_date', models.DateField(blank=True, default=None, null=True)),
                ('news_from_date', models.DateField(blank=True, default=None, null=True)),
                ('news_to_date', models.DateField(blank=True, default=None, null=True)),
                ('product_attachment_file', models.CharField(blank=True, default=None, max_length=2000, null=True)),
                ('msrp', models.FloatField(blank=True, default=1, null=True)),
                ('binrr', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('binother', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('binmr', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('bing', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('notation', models.TextField(blank=True, default=None, max_length=2000, null=True)),
                ('assoc', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('slvrcont', models.FloatField(blank=True, default=0, null=True)),
                ('unit_weight', models.FloatField(blank=True, default=0, null=True)),
                ('slvweight', models.FloatField(blank=True, default=0, null=True)),
                ('txtsilveryr', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('centurytxt', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('chksilver', models.BooleanField(default=False)),
                ('invhdate', models.DateField(blank=True, null=True)),
                ('bulk_qty', models.IntegerField(blank=True, default=0, null=True)),
                ('additional_attributes', models.JSONField(blank=True, default=dict, null=True)),
                ('call_for_price', models.BooleanField(default=False)),
                ('sort_order', models.IntegerField(blank=True, default=0, null=True)),
                ('keywords', models.CharField(blank=True, default=None, max_length=500, null=True)),
                ('seo_title', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('meta_description', models.CharField(blank=True, default=None, max_length=1000, null=True)),
                ('variable', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('circulation', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('product_id', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('variant_id', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('collections', models.ManyToManyField(related_name='products', to='vendor.collection')),
                ('setparts', models.ManyToManyField(blank=True, related_name='products', to='vendor.setpart')),
                ('tags', models.ManyToManyField(related_name='products', to='vendor.tag')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='vendor.type')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='vendor.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='LineItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_price', models.FloatField(default=0)),
                ('quantity', models.IntegerField(default=1)),
                ('item_note', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineItems', to='vendor.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineItems', to='vendor.product')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(default=None, max_length=2000)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='vendor.product')),
            ],
        ),
    ]
