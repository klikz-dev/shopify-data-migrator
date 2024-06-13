from django.core.management.base import BaseCommand

from pathlib import Path
from tqdm import tqdm

from utils import common, feed

from vendor.models import Product, Vendor, Type, Collection, Tag, Image, Setpart

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

        if "setpart" in options['functions']:
            processor.setpart()


class Processor:
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def product(self):

        Product.objects.all().delete()
        Collection.objects.all().delete()
        Type.objects.all().delete()
        Tag.objects.all().delete()
        Vendor.objects.all().delete()
        Image.objects.all().delete()

        # Get Product Feed
        column_map = {
            'sku': 'sku',
            'title': 'title',
            'description': 'long_description',

            'type': 'product_type',
            'collections': 'product_categories',
            'tags': 'product_tags',

            'wholesale': 'wholesale_price',
            'retail': 'retail_price',

            'stock': 'instock',
            'weight': 'weight',

            'status': 'status',

            'parent_sku': 'parent_sku',
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

        rows = feed.readExcel(
            file_path=f"{FILEDIR}/ecc-products-master.xlsx",
            column_map=column_map,
            exclude=[]
        )

        for row in tqdm(rows):

            sku = common.to_text(row['sku'])

            product = Product(sku=sku)

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

    def setpart(self):

        Setpart.objects.all().delete()

        # Get Set Parts Data
        column_map = {
            'parent_sku': 'parent_sku',
            'parent_order_code': 'parent_order_code',
            'sku': 'child_sku',
            'order_code': 'order_code',
            'title': 'title',
            'metal': 'metal',
            'diameter': 'diameter',
            'circulation': 'circulation',
            'assoc': 'assoc',
            'price': 'price',
            'obverse_detail': 'obverse_detail',
            'reverse_detail': 'reverse_detail',
            'info': 'full_info',
            'country': 'country',
            'unit_weight': 'unit_weight',
        }

        rows = feed.readExcel(
            file_path=f"{FILEDIR}/ecc-setpart-master.xlsx",
            column_map=column_map,
            exclude=[]
        )

        for row in tqdm(rows):
            try:
                product = Product.objects.get(
                    sku=common.to_text(row['parent_sku']))
            except Product.DoesNotExist:
                continue

            setpart, _ = Setpart.objects.get_or_create(
                sku=common.to_text(row['sku']),
                defaults={
                    'parent_order_code': common.to_text(row.get('parent_order_code')),
                    'order_code': common.to_text(row.get('order_code')),
                    'title': common.to_text(row.get('title')),
                    'metal': common.to_text(row.get('metal')),
                    'diameter': common.to_text(row.get('diameter')),
                    'circulation': common.to_text(row.get('circulation')),
                    'assoc': common.to_text(row.get('assoc')),
                    'price': common.to_float(row.get('price')),
                    'obverse_detail': common.to_text(row.get('obverse_detail')),
                    'reverse_detail': common.to_text(row.get('reverse_detail')),
                    'info': common.to_text(row.get('info')),
                    'country': common.to_text(row.get('country')),
                    'unit_weight': common.to_float(row.get('unit_weight')),
                }
            )

            setpart.products.add(product)
