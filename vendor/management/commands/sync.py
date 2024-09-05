from django.core.management.base import BaseCommand

from pathlib import Path

from utils import shopify, common
from vendor.models import Product, Customer, Order, Collection, Company

FILEDIR = f"{Path(__file__).resolve().parent.parent}/files"


class Command(BaseCommand):
    help = f"Read Product Datasheet"

    def add_arguments(self, parser):
        parser.add_argument('functions', nargs='+', type=str)

    def handle(self, *args, **options):
        processor = Processor()

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

        if "inventory" in options['functions']:
            processor.inventory()

        if "company" in options['functions']:
            processor.company()


class Processor:
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def product(self):

        products = Product.objects.all().exclude(
            type__name="Variable").filter(product_id=None)
        total = len(products)

        def sync_product(index, product):
            shopify_product = shopify.create_product(
                product=product, thread=index)

            if shopify_product.id:
                product.product_id = shopify_product.id
                product.handle = shopify_product.handle
                product.save()

                shopify.update_inventory(product=product, thread=index)
                self.image(product)

                print(
                    f"{index}/{total} -- Product {shopify_product.id} Created")

        # for index, product in enumerate(products):
        #     sync_product(index, product)

        common.thread(rows=products, function=sync_product)

    def variant(self):

        parent_skus = set(Product.objects.all().filter(
            type__name="Variable").values_list('parent_sku', flat=True).distinct())
        total = len(parent_skus)

        for index, parent_sku in enumerate(parent_skus):
            product = Product.objects.get(sku=parent_sku)

            variants = Product.objects.filter(
                parent_sku=parent_sku).filter(type__name="Variable").exclude(variable="")

            shopify_product = shopify.create_variable_product(
                product=product, variants=variants, thread=index)
            shopify_variants = shopify_product.variants

            if shopify_product.id:

                for shopify_variant in shopify_variants:
                    variant = variants.filter(
                        sku=shopify_variant.sku).first()
                    variant.product_id = shopify_product.id
                    variant.variant_id = shopify_variant.id
                    variant.save()

            print(f"{index}/{total} -- Variant {parent_sku} Created")

    def image(self, product):
        images = product.images.all()

        def sync_image(index, image):
            if image.path:
                shopify_image = shopify.upload_image(
                    product_id=product.product_id,
                    image=f"{FILEDIR}/{image.path}",
                    alt=product.title,
                    thread=index
                )

                print(
                    f"Uploaded Image {shopify_image.id} for Product {product.product_id}")

        # for index, image in enumerate(images):
        #     sync_image(index, image)

        common.thread(rows=images, function=sync_image)

    def customer(self):

        # Upload Customers
        customers = Customer.objects.all().filter(customer_id=None)
        total = len(customers)

        def sync_customer(index, customer):
            shopify_customer = shopify.create_customer(
                customer=customer, thread=index)

            if shopify_customer.id:
                customer.customer_id = shopify_customer.id
                customer.save()
                print(f"{index}/{total} -- Synced customer {shopify_customer.id}")
            else:
                print(f"Error syncing customer {customer.customer_no}")
                print(customer.phone)

        # for index, customer in enumerate(customers):
        #     sync_customer(index, customer)

        common.thread(rows=customers, function=sync_customer)

    def order(self):

        orders = Order.objects.all().filter(order_id=None)
        total = len(orders)

        def sync_order(index, order):
            shopify_order = shopify.create_order(
                order=order, thread=index)

            if shopify_order.id:
                order.order_id = shopify_order.id
                order.save()
                print(f"{index}/{total} -- Order {order.order_no} Created")

        # for index, order in enumerate(orders):
        #     sync_order(index, order)

        common.thread(rows=orders, function=sync_order)

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

    def inventory(self):

        products = Product.objects.all()
        total = len(products)

        def sync_inventory(index, product):
            try:
                if product.product_id:
                    shopify.update_inventory(
                        product=product, thread=index)

                    print(
                        f"{index}/{total} -- Product Inventory for {product.product_id} has been updated")

            except Exception as e:
                print(e)
                return

        # for index, product in enumerate(products):
        #     sync_inventory(index, product)

        common.thread(rows=products, function=sync_inventory)

    def company(self):

        companies = Company.objects.all().filter(company_id=None)
        total = len(companies)

        def sync_company(index, company):
            company_id = shopify.create_company(
                company=company, thread=index)

            if company_id:
                company.company_id = company_id
                company.save()
                print(f"{index}/{total} -- Company {company.company_name} Created")

        # for index, company in enumerate(companies):
        #     sync_company(index, company)

        common.thread(rows=companies, function=sync_company)
