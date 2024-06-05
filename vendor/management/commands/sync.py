from django.core.management.base import BaseCommand

from pathlib import Path

from utils import shopify
from vendor.models import Product

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

        products = Product.objects.all()

        def sync_product(index, product):
            if product.product_id:
                shopify_product = shopify.update_product(
                    product=product, thread=index)
                if shopify_product.handle:
                    product.handle = shopify_product.handle
                    product.save()
                    print(
                        f"Product {product.handle} has been updated successfully.")
                else:
                    print(
                        f"Failed uploading - Product {product.handle}")

            else:
                shopify_product = shopify.create_product(
                    product=product, thread=index)

                if shopify_product.id:
                    product.product_id = shopify_product.id
                    product.handle = shopify_product.handle
                    product.save()
                    print(
                        f"Product {shopify_product.id} has been created successfully.")
                else:
                    print(
                        f"Failed uploading - Product {product.handle}")

        for index, product in enumerate(products):
            sync_product(index, product)
