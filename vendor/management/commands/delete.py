from django.core.management.base import BaseCommand

from pathlib import Path

from utils import shopify, common


class Command(BaseCommand):
    help = f"Delete from Shopify"

    def add_arguments(self, parser):
        parser.add_argument('functions', nargs='+', type=str)

    def handle(self, *args, **options):
        processor = Processor()

        if "order" in options['functions']:
            processor.order()

        if "customer" in options['functions']:
            processor.customer()

        if "product" in options['functions']:
            processor.product()


class Processor:
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def order(self):
        all_order_ids = shopify.list_orders()

        def delete_order(index, order_id):
            print(f"Deleting {order_id}")
            shopify.delete_order(order_id, thread=index)

        common.thread(rows=all_order_ids, function=delete_order)

    def customer(self):
        all_customer_ids = shopify.list_customers()

        def delete_customer(index, customer_id):
            print(f"Deleting {customer_id}")
            shopify.delete_customer(customer_id, thread=index)

        common.thread(rows=all_customer_ids, function=delete_customer)

    def product(self):
        all_product_ids = shopify.list_products()

        def delete_product(index, product_id):
            print(f"Deleting {product_id}")
            shopify.delete_product(product_id, thread=index)

        common.thread(rows=all_product_ids, function=delete_product)
