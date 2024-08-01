from django.core.management.base import BaseCommand

import os
from shopify import Session as ShopifySession, Product as ShopifyProduct, Customer as ShopifyCustomer, Order as ShopifyOrder

from utils import shopify, common

SHOPIFY_API_BASE_URL = os.getenv('SHOPIFY_API_BASE_URL')
SHOPIFY_API_VERSION = os.getenv('SHOPIFY_API_VERSION')
SHOPIFY_API_TOKEN = os.getenv('SHOPIFY_API_TOKEN')
SHOPIFY_API_THREAD_TOKENS = os.getenv('SHOPIFY_API_THREAD_TOKENS')


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
        def delete_order(index, order_id):
            print(f"Deleting Order {order_id}")
            shopify.delete_order(order_id, thread=index)

        processor = shopify.Processor()
        with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):
            shopify_orders = ShopifyOrder.find(limit=250, status="any")

            while shopify_orders:
                print(f"Fetched {len(shopify_orders)} Orders.")

                shopify_order_ids = []
                for shopify_order in shopify_orders:
                    shopify_order_ids.append(shopify_order.id)

                common.thread(rows=shopify_order_ids, function=delete_order)

                shopify_orders = shopify_orders.has_next_page() and shopify_orders.next_page() or []

    def customer(self):
        def delete_customer(index, customer_id):
            print(f"Deleting {customer_id}")
            shopify.delete_customer(customer_id, thread=index)

        processor = shopify.Processor()
        with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):
            shopify_customers = ShopifyCustomer.find(limit=250, status="any")

            while shopify_customers:
                print(f"Fetched {len(shopify_customers)} Customers.")

                shopify_customer_ids = []
                for shopify_customer in shopify_customers:
                    shopify_customer_ids.append(shopify_customer.id)

                common.thread(rows=shopify_customer_ids,
                              function=delete_customer)

                shopify_customers = shopify_customers.has_next_page(
                ) and shopify_customers.next_page() or []

    def product(self):
        def delete_product(index, product_id):
            print(f"Deleting {product_id}")
            shopify.delete_product(product_id, thread=index)

        processor = shopify.Processor()
        with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):
            shopify_products = ShopifyProduct.find(limit=250)

            while shopify_products:
                print(f"Fetched {len(shopify_products)} Products.")

                shopify_product_ids = []
                for shopify_product in shopify_products:
                    shopify_product_ids.append(shopify_product.id)

                common.thread(rows=shopify_product_ids,
                              function=delete_product)

                shopify_products = shopify_products.has_next_page(
                ) and shopify_products.next_page() or []
