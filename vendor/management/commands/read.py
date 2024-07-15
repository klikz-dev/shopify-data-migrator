from django.core.management.base import BaseCommand

from pathlib import Path
from tqdm import tqdm

from utils import common, feed

from vendor.models import Product, Vendor, Type, Collection, Tag, Image, Setpart, Customer, Order, LineItem

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

        if "customer" in options['functions']:
            processor.customer()

        if "customer-update" in options['functions']:
            processor.customer_update()

        if "order" in options['functions']:
            processor.order()


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

        # Read Product Details
        details = {}

        column_map = {
            'sku': 'StockID',

            'binrr': 'BINRR',
            'binother': 'BINOther',
            'binmr': 'BINMR',
            'bing': 'BING',
            'notation': 'NOTATION',

            'quantity': 'BINH',
        }

        rows = feed.readExcel(
            file_path=f"{FILEDIR}/ecc-inventory-master.xlsx",
            column_map=column_map,
            exclude=[],
            get_other_attributes=False
        )

        for row in tqdm(rows):
            sku = common.to_text(row['sku'])

            binrr = common.to_text(row['binrr'])
            binother = common.to_text(row['binother'])
            binmr = common.to_text(row['binmr'])
            bing = common.to_text(row['bing'])
            notation = common.to_text(row['notation'])

            quantity = common.to_int(row['quantity'])

            details[sku] = {
                'binrr': binrr,
                'binother': binother,
                'binmr': binmr,
                'bing': bing,
                'notation': notation,
                'quantity': quantity
            }

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
            'add_box': 'add_box',
            'show_component': 'show_component',
            'track_qty': 'track_qty',
            'bulk_qty': 'bulk_qty',

            'parent_sku': 'parent_sku',
            'length': 'length',
            'height': 'height',
            'country': 'country',
            'order_code': 'order_code',
            'dimensions': 'dimensions',
            'denomination': 'denomination',
            'era': 'era',
            'variable': 'variable',
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
            'note': 'notes',

            'images': 'images',
        }

        rows = feed.readExcel(
            file_path=f"{FILEDIR}/ecc-products-master.xlsx",
            column_map=column_map,
            exclude=[]
        )

        for row in tqdm(rows):

            sku = common.to_text(row['sku'])
            title = common.to_text(row['title'])
            order_code = common.to_text(row.get('order_code'))

            if not sku or not order_code:
                continue
            if not title:
                title = order_code

            try:
                product = Product.objects.get(sku=sku)
            except Product.DoesNotExist:
                product = Product(sku=sku)

            product.title = title
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
            product.quantity = details.get(sku, {}).get('quantity', 0)
            product.weight = common.to_float(row['weight'])

            # Status
            product.status = common.to_text(row['status']) == "publish"
            product.add_box = row['add_box'] == True
            product.show_component = row['show_component'] == True
            product.track_qty = row['track_qty'] == True

            # Attributes
            product.parent_sku = common.to_text(row.get('parent_sku'))
            product.length = common.to_float(row.get('length'))
            product.height = common.to_float(row.get('height'))
            product.country = common.to_text(row.get('country'))
            product.order_code = order_code
            product.dimensions = common.to_text(row.get('dimensions'))
            product.denomination = common.to_text(row.get('denomination'))
            product.era = common.to_text(row.get('era'))
            product.variable = common.to_text(row.get('variable'))
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
            product.binrr = details.get(sku, {}).get('binrr', "")
            product.binother = details.get(sku, {}).get('binother', "")
            product.binmr = details.get(sku, {}).get('binmr', "")
            product.bing = details.get(sku, {}).get('bing', "")
            product.notation = details.get(sku, {}).get('notation', "")
            product.bulk_qty = common.to_int(row['bulk_qty'])
            product.additional_attributes = row['attributes']

            # Images
            images = common.to_text(row['images']).split("|")
            for image in images:
                if image:
                    Image.objects.create(product=product, path=image)

            # Write Feed
            product.save()

    def setpart(self):

        Setpart.objects.all().delete()

        # Get Set Parts Data
        column_map = {
            'parent_sku': 'parent_sku',

            'sku': 'child_sku',
            'order_code': 'order_code',
            'title': 'title',
            'parent_order_code': 'parent_order_code',
        }

        rows = feed.readExcel(
            file_path=f"{FILEDIR}/ecc-setpart-master.xlsx",
            column_map=column_map,
            exclude=[]
        )

        for row in tqdm(rows):
            parent_sku = common.to_text(row['parent_sku'])
            try:
                product = Product.objects.get(
                    sku=parent_sku)
            except Product.DoesNotExist:
                # print(f"{parent_sku} Not found")
                continue

            setpart, _ = Setpart.objects.get_or_create(
                sku=common.to_text(row['sku']),
                defaults={
                    'order_code': common.to_text(row.get('order_code')),
                    'title': common.to_text(row.get('title')),
                    'parent_order_code': common.to_text(row.get('parent_order_code')),
                }
            )

            setpart.products.add(product)

    def customer(self):
        Customer.objects.all().delete()

        column_map = {
            'customer_no': 'CUSTNUM',
            'email': 'email',
            'phone': 'PHONE',
            'first_name': 'FIRSTNAME',
            'last_name': 'LASTNAME',
            'company': 'COMPANY',
            'address1': 'ADDR',
            'address2': 'ADDR2',
            'city': 'CITY',
            'state': 'STATE',
            'zip': 'ZIPCODE',
            'country': 'COUNTRY',
            'note': 'COMMENT',

            'trade_show_sales_representative': 'chkComm',
            'payment_terms': 'DUE_DAYS',
            'vat_no': 'vatNumber',
            'orig_ad': 'ORIG_AD',
            'check_dropship': 'chkCustDropShip',
            'additional_attributes': 'additional_attributes',
        }

        rows = feed.readExcel(
            file_path=f"{FILEDIR}/ecc-customers-master.xlsx",
            column_map=column_map,
            exclude=[]
        )

        for row in tqdm(rows):

            customer_no = common.to_int(row.get('customer_no'))

            if customer_no == 0:
                continue

            try:
                customer = Customer.objects.get(customer_no=customer_no)
            except Customer.DoesNotExist:
                customer = Customer(customer_no=customer_no)

            customer.email = common.to_text(row.get('email'))
            customer.first_name = common.to_text(row.get('first_name'))
            customer.last_name = common.to_text(row.get('last_name'))
            customer.company = common.to_text(row.get('company'))
            customer.address1 = common.to_text(row.get('address1'))
            customer.address2 = common.to_text(row.get('address2'))
            customer.city = common.to_text(row.get('city'))
            customer.state = common.to_text(row.get('state'))
            customer.zip = common.to_text(row.get('zip'))
            customer.country = common.to_country(
                common.to_text(row.get('country')))
            customer.phone = common.to_phone(
                customer.country, common.to_text(row.get('phone')))
            customer.note = common.to_text(row.get('note'))

            customer.trade_show_sales_representative = row.get(
                'trade_show_sales_representative')
            customer.payment_terms = common.to_int(row.get('payment_terms'))
            customer.vat_no = common.to_text(row.get('vat_no'))
            customer.orig_ad = common.to_text(row.get('orig_ad'))
            customer.check_dropship = row.get('check_dropship')
            customer.additional_attributes = row.get('attributes')

            customer.save()

    def customer_update(self):

        column_map = {
            'customer_no': 'ECC Customer Number',
            'email': 'User Email',
            'customer_type': 'Type',
        }

        rows = feed.readExcel(
            file_path=f"{FILEDIR}/ecc-customers-master-update.xlsx",
            column_map=column_map,
            exclude=[]
        )

        for row in tqdm(rows):

            customer_no = common.to_int(row.get('customer_no'))
            email = common.to_text(row.get('email'))

            try:
                if customer_no > 0:
                    customer = Customer.objects.get(customer_no=customer_no)
                elif email:
                    customer = Customer.objects.get(email=email)
                else:
                    continue
            except Customer.DoesNotExist:
                continue
            except:
                continue

            customer_type = common.to_text(row.get('customer_type')).lower()
            if customer_type:
                customer.customer_type = customer_type
                customer.tags = customer_type

            customer.save()

    def order(self):

        Order.objects.all().delete()

        column_map = {
            'order_no': 'Order Number',
            'order_date': 'Order Date',
            'order_total': 'Order Total',
            'terms': 'Terms',
            'terms_due_date': 'Terms Due Date',
            'sku': 'SKU #',
            'order_code': 'Order Code',
            'quantity': 'Quantity',
            'unit_price': 'Unit Price',
            'item_note': 'Item Note',
            'payment_method': 'Payment Method',
            'card_type': 'Card Type',
            'approval': 'APPROVAL',
            'shipping_method': 'Shipping Method',
            'shipping_cost': 'Shipping cost',
            'order_memo': 'Order Memo',
            'customer_no': 'Customer Number',
            'company': 'Company',
            'amount_paid': 'Amount Paid',
            'po_number': 'PO Number',
            'tracking_number': 'tracking_number',
            'sales_rep_robin': 'Sales Rep Robin',
        }

        rows = feed.readExcel(
            file_path=f"{FILEDIR}/ecc-order-history-master.xlsx",
            column_map=column_map,
            exclude=[]
        )

        for row in tqdm(rows):

            order_no = common.to_int(row['order_no'])
            customer_no = common.to_text(row['customer_no'])
            sku = common.to_text(row['sku'])

            if not order_no:
                continue

            try:
                product = Product.objects.get(sku=sku)
            except Product.DoesNotExist:
                continue

            try:
                customer = Customer.objects.get(customer_no=customer_no)
            except Customer.DoesNotExist:
                continue

            order, _ = Order.objects.get_or_create(
                order_no=order_no,
                defaults={
                    'customer': customer,
                    'order_date': row.get('order_date'),
                    'order_total': common.to_float(row.get('order_total')),
                    'terms': common.to_text(row.get('terms')),
                    'terms_due_date': common.to_date(row.get('terms_due_date')),
                    'order_code': common.to_text(row.get('order_code')),
                    'payment_method': common.to_text(row.get('payment_method')),
                    'card_type': common.to_text(row.get('card_type')),
                    'approval': common.to_text(row.get('approval')),
                    'shipping_method': common.to_text(row.get('shipping_method')),
                    'shipping_cost': common.to_float(row.get('shipping_cost')),
                    'order_memo': common.to_text(row.get('order_memo')),
                    'customer_no': common.to_text(row.get('customer_no')),
                    'company': common.to_text(row.get('company')),
                    'amount_paid': common.to_float(row.get('amount_paid')),
                    'po_number': common.to_text(row.get('po_number')),
                    'tracking_number': common.to_text(row.get('tracking_number')),
                    'sales_rep_robin': row.get('sales_rep_robin') == True
                }
            )

            LineItem.objects.create(
                order=order,
                product=product,
                unit_price=common.to_float(row['unit_price']),
                quantity=common.to_int(row['quantity']),
                item_note=common.to_text(row['item_note']),
            )
