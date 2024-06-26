from django.core.management.base import BaseCommand

from pathlib import Path
from tqdm import tqdm
import pycountry

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
                row['stock']) == "instock" else 0
            product.weight = common.to_float(row['weight'])

            # Status
            product.status = common.to_text(row['status']) == "publish"
            product.add_box = common.to_text(row['add_box']) == True
            product.show_component = common.to_text(
                row['show_component']) == True
            product.track_qty = common.to_text(row['track_qty']) == True

            # Attributes
            product.parent_sku = common.to_text(row.get('parent_sku'))
            product.length = common.to_float(row.get('length'))
            product.height = common.to_float(row.get('height'))
            product.country = common.to_text(row.get('country'))
            product.order_code = common.to_text(row.get('order_code'))
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
            product.note = common.to_text(row.get('note'))
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

            'sku': 'child_sku',
            'order_code': 'order_code',
            'title': 'title',
            'parent_order_code': 'parent_order_code',
            # 'metal': 'metal',
            # 'diameter': 'diameter',
            # 'circulation': 'circulation',
            # 'assoc': 'assoc',
            # 'price': 'price',
            # 'obverse_detail': 'obverse_detail',
            # 'reverse_detail': 'reverse_detail',
            # 'info': 'full_info',
            # 'country': 'country',
            # 'unit_weight': 'unit_weight',
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
                    # 'metal': common.to_text(row.get('metal')),
                    # 'diameter': common.to_text(row.get('diameter')),
                    # 'circulation': common.to_text(row.get('circulation')),
                    # 'assoc': common.to_text(row.get('assoc')),
                    # 'price': common.to_float(row.get('price')),
                    # 'obverse_detail': common.to_text(row.get('obverse_detail')),
                    # 'reverse_detail': common.to_text(row.get('reverse_detail')),
                    # 'info': common.to_text(row.get('info')),
                    # 'country': common.to_text(row.get('country')),
                    # 'unit_weight': common.to_float(row.get('unit_weight')),
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
            'comm': 'chkComm'
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

            email = common.to_text(row.get('email'))
            phone = common.to_text(row.get('phone'))

            first_name = common.to_text(row.get('first_name'))
            last_name = common.to_text(row.get('last_name'))
            company = common.to_text(row.get('company'))

            address1 = common.to_text(row.get('address1'))
            address2 = common.to_text(row.get('address2'))
            city = common.to_text(row.get('city'))
            state = common.to_text(row.get('state'))
            zip = common.to_text(row.get('zip'))
            country_code = common.to_text(row.get('country'))

            note = common.to_text(row.get('note'))
            comm = row.get('comm')

            # fine-tune
            country = common.to_country(country_code)
            phone = common.to_phone(country, phone)

            if not email and not phone:
                continue

            customer = Customer(
                customer_no=customer_no,
                email=email,
                phone=phone,
                first_name=first_name,
                last_name=last_name,
                company=company,
                address1=address1,
                address2=address2,
                city=city,
                state=state,
                zip=zip,
                country=country,
                note=note,
                comm=comm,
            )

            customer.save()

    def customer_update(self):

        column_map = {
            'customer_no': 'ECC Customer Number',
            'email': 'User Email',
            'phone': 'Billing Phone',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'company': 'Shipping Company',
            'address1': 'Shipping Address 1',
            'address2': 'Shipping Address 2',
            'city': 'Shipping City',
            'state': 'Shipping State',
            'zip': 'Shipping Postcode',
            'country': 'Shipping Country',
            'type': 'Type',
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

            if email:
                customer.email = email

            phone = common.to_text(row.get('phone'))
            if phone:
                customer.phone = phone

            first_name = common.to_text(row.get('first_name'))
            if first_name:
                customer.first_name = phone

            last_name = common.to_text(row.get('last_name'))
            if last_name:
                customer.last_name = last_name

            company = common.to_text(row.get('company'))
            if company:
                customer.company = company

            address1 = common.to_text(row.get('address1'))
            if address1:
                customer.address1 = address1

            address2 = common.to_text(row.get('address2'))
            if address2:
                customer.address2 = address2

            city = common.to_text(row.get('city'))
            if city:
                customer.city = city

            state = common.to_text(row.get('state'))
            if state:
                customer.state = state

            zip = common.to_text(row.get('zip'))
            if zip:
                customer.zip = zip

            country = common.to_text(row.get('country'))
            if country:
                customer.country = country

            type = common.to_text(row.get('type')).lower()
            if type:
                customer.type = type
                customer.tags = type

            customer.save()

    def order(self):

        Order.objects.all().delete()

        column_map = {
            'order_no': 'ORDERid',
            'shipping': 'TB_SHIP',
            'shipping_method': 'SHIPLIST',
            'total': 'AMT_PAID',
            'order_date': 'ODR_DATE',
            'note': 'OrderMemo',

            'unit_price': 'IT_UNLIST',
            'discount': 'DISCOUNT',
            'quantity': 'QUANTO',

            'customer_no': 'tblCMS_CUSTNUM',
            'order_code': 'ITEM',
        }

        rows = feed.readExcel(
            file_path=f"{FILEDIR}/ecc-orders-master.xlsx",
            column_map=column_map,
            exclude=[]
        )

        for row in tqdm(rows):

            order_no = common.to_int(row['order_no'])
            if not order_no:
                continue

            order_code = common.to_text(row['order_code'])
            customer_no = common.to_text(row['customer_no'])

            if "(" in order_code:
                circulation = f'({order_code.split("(")[1]}'
                order_code = order_code.split("(")[0]
            else:
                circulation = ""
                order_code = order_code

            try:
                product = Product.objects.filter(
                    order_code=order_code, circulation=circulation).first()
            except Product.DoesNotExist:
                continue

            if not product:
                continue

            try:
                customer = Customer.objects.get(customer_no=customer_no)
            except Customer.DoesNotExist:
                continue

            order, _ = Order.objects.get_or_create(
                order_no=order_no,
                defaults={
                    'customer': customer,
                    'shipping': common.to_float(row['shipping']),
                    'shipping_method': common.to_text(row['shipping_method']),
                    'total': common.to_float(row['total']),
                    'order_date': row['order_date'],
                    'note': common.to_text(row['note']),
                }
            )

            LineItem.objects.create(
                order=order,
                product=product,
                unit_price=common.to_float(row['unit_price']),
                discount=common.to_float(row['discount']),
                quantity=common.to_int(row['quantity']),
            )
