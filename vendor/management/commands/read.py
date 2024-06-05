from django.core.management.base import BaseCommand

import os
from pathlib import Path
import re

from utils import common, feed

from vendor.models import Product, Vendor, Type, Collection, Tag, Image

FILEDIR = f"{Path(__file__).resolve().parent.parent}/files"
IMAGEDIR = f"{Path(__file__).resolve().parent.parent}/files/images"


class Command(BaseCommand):
    help = f"Read Product Datasheet"

    def add_arguments(self, parser):
        parser.add_argument('functions', nargs='+', type=str)

    def handle(self, *args, **options):
        processor = Processor()

        if "product" in options['functions']:
            processor.product()


class Processor:
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def product(self):

        # Get Product Feed
        column_map = {
            'sku': 'sku',
            'title': 'title_description',
            'description': 'long_description',

            'type': 'product_type',
            'collections': 'category',
            'tags': 'product tags',

            'wholesale': 'wholesale_price',
            'retail': 'retail_price',

            'stock': 'instock',
            'weight': 'weight',

            'status': 'status',

            'parent_sku': 'parent sku',
            'category': 'category',
            'length': 'length',
            'height': 'height',
            'country': 'country',
            'order_code': 'order_code',
            'dimensions': 'dimensions',
            'era': 'era',
            'circulation': 'circulation',
            'metal': 'metal',
            'misc_product_info': 'misc_product_info',
            'obverse_detail': 'obverse_detail',
            'region': 'region',
            'reverse_detail': 'reverse_detail',
            'ruler': 'ruler',
            'size': 'size',
            'subcategory': 'subcategory',
            'custom_date': 'custom_date',
            'news_from_date': 'news_from_date',
            'news_to_date': 'news_to_date',
            'product_attachment_file': 'product_attachment_file',
            'msrp': 'msrp',

            'images': 'images',
        }

        exclude = [
            'wholesale_price',
            'dropshipper_fixed_price_rules',
            'dropshipper_tiered_price_minimum_qty',
            'wholesale_tiered_price_regular_price',
            'wholesale_fixed_price_rules',
            'wholesale_tiered_price_minimum_qty calculated',
            'fixed_price_rules',
            'tiered_price_minimum_qty',
            'product_addons_exclude_global',
            'hidden',
            'product_attachment_file',
            'sort_order',
            'bundle_items',
            'subcat3',
            'subcat4',
            'subcat5',
            'gallery1',
            'gallery2',
            'gallery',
            'noImport',
            'Focus Keyphrase in table web promo',
            'SEO Title in table web promo',
            'Meta Description in table web promo',
            'bulk_qty',
        ]

        rows = feed.readExcel(
            file_path=f"{FILEDIR}/mid-sized-albums.xlsx",
            column_map=column_map,
            exclude=exclude
        )

        Product.objects.all().delete()
        Collection.objects.all().delete()
        Type.objects.all().delete()
        Tag.objects.all().delete()
        Vendor.objects.all().delete()

        for row in rows:
            print(row['sku'])

            product = Product(
                sku=common.to_text(row['sku'])
            )

            product.title = common.to_text(row['title'])
            product.handle = common.to_handle(product.title)
            product.description = common.to_text(row['description'])

            vendor, _ = Vendor.objects.get_or_create(name="Educational Coin")
            product.vendor = vendor

            # Type
            type = common.to_text(row['type']).title()
            type, _ = Type.objects.get_or_create(name=type)
            product.type = type

            product.save()

            # Collections
            collections = common.to_text(row['collections']).split(",")
            for collectionText in collections:
                if ">" in collectionText:
                    parent = common.to_text(collectionText.split('>')[0])
                    name = common.to_text(collectionText.split('>')[1])

                    collection, _ = Collection.objects.get_or_create(name=name)
                    parentCollection, _ = Collection.objects.get_or_create(
                        name=parent)

                    collection.parents.add(parentCollection)
                else:
                    collection, _ = Collection.objects.get_or_create(
                        name=common.to_text(collectionText))

                product.collections.add(collection)

            # Tags
            tags = common.to_text(row['tags']).split(",")
            for tagText in tags:
                tag, _ = Tag.objects.get_or_create(name=tagText)
                product.tags.add(tag)

            # Price
            product.wholesale = common.to_float(row['wholesale'])
            product.retail = common.to_float(row['retail'])

            # Inventory & Shipping
            product.quantity = 1000 if common.to_text(
                row['stock']).lower() == "instock" else 0
            product.weight = common.to_float(row['weight'])

            # Status
            product.status = common.to_text(row['status']).lower() == "publish"

            # Attributes
            product.parent_sku = common.to_text(row.get('parent_sku'))
            product.category = common.to_text(row.get('category'))
            product.length = common.to_float(row.get('length'))
            product.height = common.to_float(row.get('height'))
            product.country = common.to_text(row.get('country'))
            product.order_code = common.to_text(row.get('order_code'))
            product.dimensions = common.to_text(row.get('dimensions'))
            product.era = common.to_text(row.get('era'))
            product.circulation = common.to_text(row.get('circulation'))
            product.metal = common.to_text(row.get('metal'))
            product.misc_product_info = common.to_text(
                row.get('misc_product_info'))
            product.obverse_detail = common.to_text(row.get('obverse_detail'))
            product.region = common.to_text(row.get('region'))
            product.reverse_detail = common.to_text(row.get('reverse_detail'))
            product.ruler = common.to_text(row.get('ruler'))
            product.size = common.to_text(row.get('size'))
            product.subcategory = common.to_text(row.get('subcategory'))
            product.custom_date = common.to_date(row.get('custom_date'))
            product.news_from_date = common.to_date(row.get('news_from_date'))
            product.news_to_date = common.to_date(row.get('news_to_date'))
            product.product_attachment_file = common.to_text(
                row.get('product_attachment_file'))
            product.msrp = common.to_float(row.get('msrp'))
            product.additional_attributes = row['attributes']

            # Images
            images = common.to_text(row['images']).split("|")
            for image in images:
                Image.objects.create(product=product, path=image)

            # Write Feed
            product.save()
