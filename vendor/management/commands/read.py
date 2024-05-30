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
            'sku': 'parent sku',
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

            'order_code': 'order_code',

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
            'msrp',
            'subcategory',
            'sku',
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
                sku=common.toText(row['sku'])
            )

            product.title = common.toText(row['title'])
            product.handle = common.toHandle(product.title)
            product.description = common.toText(row['description'])

            vendor, _ = Vendor.objects.get_or_create(name="Educational Coin")
            product.vendor = vendor

            # Type
            type = common.toText(row['type']).title()
            type, _ = Type.objects.get_or_create(name=type)
            product.type = type

            product.save()

            # Collections
            collections = common.toText(row['collections']).split(",")
            for collectionText in collections:
                if ">" in collectionText:
                    parent = common.toText(collectionText.split('>')[0])
                    name = common.toText(collectionText.split('>')[1])

                    collection, _ = Collection.objects.get_or_create(name=name)
                    parentCollection, _ = Collection.objects.get_or_create(
                        name=parent)

                    collection.parents.add(parentCollection)
                else:
                    collection, _ = Collection.objects.get_or_create(
                        name=common.toText(collectionText))

                product.collections.add(collection)

            # Tags
            tags = common.toText(row['tags']).split(",")
            for tagText in tags:
                tag, _ = Tag.objects.get_or_create(name=tagText)
                product.tags.add(tag)

            # Price
            product.wholesale = common.toFloat(row['wholesale'])
            product.retail = common.toFloat(row['retail'])

            # Inventory & Shipping
            product.quantity = 1000 if common.toText(
                row['stock']).lower() == "instock" else 0
            product.weight = common.toFloat(row['weight'])

            # Status
            product.status = common.toText(row['status']).lower() == "publish"

            # Attributes
            product.order_code = common.toText(row['order_code'])
            product.attributes = row['attributes']

            # Images
            images = common.toText(row['images']).split("|")
            for image in images:
                Image.objects.create(product=product, path=image)

            # Write Feed
            product.save()
