from django.core.management.base import BaseCommand

from pathlib import Path

from utils import shopify, common
from vendor.models import Product, Customer, Order

FILEDIR = f"{Path(__file__).resolve().parent.parent}/files"


class Command(BaseCommand):
    help = f"Read Product Datasheet"

    def add_arguments(self, parser):
        parser.add_argument('functions', nargs='+', type=str)

    def handle(self, *args, **options):
        processor = Processor()

        if "product" in options['functions']:
            processor.product()

        if "customer" in options['functions']:
            processor.customer()

        if "order" in options['functions']:
            processor.order()


class Processor:
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def delete(self):
        # Delete All Customers
        all_customers = shopify.list_customers()

        def delete_customer(index, customer):
            print(f"Deleting {customer.id}")
            shopify.delete_customer(customer.id, thread=index)

        common.thread(rows=all_customers, function=delete_customer)

    def product(self):

        products = Product.objects.all()

        def sync_product(index, product):
            try:
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
                    shopify_product, shopify_variant = shopify.create_product(
                        product=product, thread=index)

                    if shopify_product.id:
                        product.product_id = shopify_product.id
                        product.variant_id = shopify_variant.id
                        product.handle = shopify_product.handle
                        product.save()

                        self.image(product)

                        print(
                            f"Product {shopify_product.id} has been created successfully.")
                    else:
                        print(
                            f"Failed uploading - Product {product.handle}")

            except Exception as e:
                print(e)
                return

        # for index, product in enumerate(products):
        #     sync_product(index, product)

        common.thread(rows=products, function=sync_product)

    def image(self, product):
        images = product.images.all()

        def sync_image(index, image):
            try:
                shopify_image = shopify.upload_image(
                    product_id=product.product_id,
                    image=f"{FILEDIR}/{image.path}",
                    alt=product.title,
                    thread=index
                )

                print(
                    f"Uploaded Image {shopify_image.id} for Product {product.product_id}")

            except Exception as e:
                print(e)
                return

        # for index, image in enumerate(images):
        #     sync_image(index, image)

        common.thread(rows=images, function=sync_image)

    def customer(self):

        # Upload Customers
        customers = Customer.objects.all()

        def sync_customer(index, customer):
            if customer.customer_id:
                shopify_customer = shopify.update_customer(
                    customer=customer, thread=index)
            else:
                shopify_customer = shopify.create_customer(
                    customer=customer, thread=index)

            if shopify_customer.id:
                customer.customer_id = shopify_customer.id
                customer.save()
                print(f"Synced customer {shopify_customer.id}")
            else:
                print(f"Error syncing customer {customer.customer_no}")
                print(customer.phone)

        # for index, customer in enumerate(customers):
        #     sync_customer(index, customer)

        common.thread(rows=customers, function=sync_customer)

    def order(self):

        orders = Order.objects.all().filter(order_id=None)

        def sync_order(index, order):
            if order.order_id:
                shopify_order = shopify.update_order(
                    order=order, thread=index)
            else:
                shopify_order = shopify.create_order(
                    order=order, thread=index)

            if shopify_order.id:
                order.order_id = shopify_order.id
                order.save()
                print(f"Synced order {shopify_order.id}")

        for index, order in enumerate(orders):
            sync_order(index, order)
            break

        # common.thread(rows=orders, function=sync_order)
