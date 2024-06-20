from django.core.management.base import BaseCommand

from pathlib import Path

from utils import shopify, common
from vendor.models import Product, Customer, Order, Collection

FILEDIR = f"{Path(__file__).resolve().parent.parent}/files"


class Command(BaseCommand):
    help = f"Read Product Datasheet"

    def add_arguments(self, parser):
        parser.add_argument('functions', nargs='+', type=str)

    def handle(self, *args, **options):
        processor = Processor()

        if "delete" in options['functions']:
            processor.delete()

        if "product" in options['functions']:
            processor.product()

        if "variant" in options['functions']:
            processor.variant()

        if "customer" in options['functions']:
            processor.customer()

        if "order" in options['functions']:
            processor.order()

        if "collection" in options['functions']:
            processor.collection()


class Processor:
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def delete(self):
        # Delete All Orders
        # all_orders = shopify.list_orders()

        # def delete_order(index, order):
        #     print(f"Deleting {order.id}")
        #     shopify.delete_order(order.id, thread=index)

        # common.thread(rows=all_orders, function=delete_order)

        # Delete All Customers
        # all_customers = shopify.list_customers()

        # def delete_customer(index, customer):
        #     print(f"Deleting {customer.id}")
        #     shopify.delete_customer(customer.id, thread=index)

        # common.thread(rows=all_customers, function=delete_customer)

        # Delete All Products
        # all_products = shopify.list_products()

        # def delete_product(index, product):
        #     print(f"Deleting {product.id}")
        #     shopify.delete_product(product.id, thread=index)

        # common.thread(rows=all_products, function=delete_product)

        pass

    def product(self):

        products = Product.objects.all().filter(type__name="Simple")

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
                    shopify_product = shopify.create_product(
                        product=product, thread=index)
                    shopify_variant = shopify_product.variants[0]

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

    def variant(self):

        parent_skus = set(Product.objects.all().filter(
            type__name="Variable").values_list('parent_sku', flat=True).distinct())

        for index, parent_sku in enumerate(parent_skus):
            print(parent_sku)

            variants = Product.objects.filter(
                parent_sku=parent_sku).filter(type__name="Variable")

            shopify_product = shopify.create_variable_product(
                variants=variants, thread=index)
            shopify_variants = shopify_product.variants

            print(shopify_product)
            print(shopify_variants)

            if shopify_product.id:

                for shopify_variant in shopify_variants:
                    variant = Product.objects.get(sku=shopify_variant.sku)
                    variant.product_id = shopify_product.id
                    variant.variant_id = shopify_variant.id
                    variant.save()

            self.image(variants.first())

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

    def collection(self):
        collections = Collection.objects.all()
        for index, collection in enumerate(collections):
            title = collection.name
            rules = [{
                'column': "tag",
                'relation': "equals",
                'condition': f"Collection:{title}",
            }]

            shopify_collection = shopify.create_collection(
                title=title, rules=rules, thread=index)

            print(
                f"Collection {shopify_collection.id} has been setup successfully")
