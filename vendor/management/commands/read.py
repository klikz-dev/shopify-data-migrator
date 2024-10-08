from django.core.management.base import BaseCommand

from pathlib import Path
from tqdm import tqdm

from utils import common, feed, shopify

from vendor.models import Product, Vendor, Type, Collection, Tag, Image, Setpart, Customer, Order, LineItem, Company

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

            'assoc': 'ASSOC',
            'slvrcont': 'slvrCont',
            'unit_weight': 'UNITWEIGHT',
            'slvweight': 'slvWeight',
            'txtsilveryr': 'txtSilverYr',
            'centurytxt': 'CenturyTxt',
            'chksilver': 'chkSilver',
            'invhdate': 'invHdate',
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

            assoc = common.to_text(row['assoc'])
            slvrcont = common.to_float(row['slvrcont'])
            unit_weight = common.to_float(row['unit_weight'])
            slvweight = common.to_float(row['slvweight'])
            txtsilveryr = common.to_text(row['txtsilveryr'])
            centurytxt = common.to_text(row['centurytxt'])
            chksilver = row['chksilver'] == True
            invhdate = common.to_date(row['invhdate'])

            details[sku] = {
                'binrr': binrr,
                'binother': binother,
                'binmr': binmr,
                'bing': bing,
                'notation': notation,
                'quantity': quantity,

                'assoc': assoc,
                'slvrcont': slvrcont,
                'unit_weight': unit_weight,
                'slvweight': slvweight,
                'txtsilveryr': txtsilveryr,
                'centurytxt': centurytxt,
                'chksilver': chksilver,
                'invhdate': invhdate,
            }

        # Get Product Feed
        column_map = {
            'sku': 'SKU',
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

            'call_for_price': 'call_for_price',
            'sort_order': 'sort_order',
            'keywords': 'keywords',
            'seo_title': 'seo_title',
            'meta_description': 'meta_description',
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

            product.assoc = details.get(sku, {}).get('assoc', "")
            product.slvrcont = details.get(sku, {}).get('slvrcont', 0)
            product.unit_weight = details.get(sku, {}).get('unit_weight', 0)
            product.slvweight = details.get(sku, {}).get('slvweight', 0)
            product.txtsilveryr = details.get(sku, {}).get('txtsilveryr', "")
            product.centurytxt = details.get(sku, {}).get('centurytxt', "")
            product.chksilver = details.get(sku, {}).get('chksilver', False)
            product.invhdate = details.get(sku, {}).get('invhdate', None)

            product.bulk_qty = common.to_int(row['bulk_qty'])
            product.additional_attributes = row['attributes']

            product.call_for_price = row.get('call_for_price') == True
            product.sort_order = common.to_int(row.get('sort_order'))
            product.keywords = common.to_text(row.get('keywords'))
            product.seo_title = common.to_text(row.get('seo_title'))
            product.meta_description = common.to_text(row.get('meta_description'))

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
                'trade_show_sales_representative') == True
            customer.payment_terms = common.to_int(row.get('payment_terms'))
            customer.vat_no = common.to_text(row.get('vat_no'))
            customer.orig_ad = common.to_text(row.get('orig_ad'))
            customer.check_dropship = row.get('check_dropship') == True
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
        LineItem.objects.all().delete()

        column_map = {
            'order_no': 'Order Number',
            'order_date': 'Order Date',
            'order_total': 'Order Total',
            'terms': 'Terms',
            'terms_due_date': 'Terms Due Date',
            'sku': 'SKU #',
            'order_code': 'Order Code',
            'discount': 'Discount',
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
            'customer_email': 'tblCust_email',
            'company': 'Company',
            'amount_paid': 'Amount Paid',
            'po_number': 'PO Number',
            'tracking_number': 'tracking_number',
            'check_number': 'CheckNum',
            'sales_rep_robin': 'Sales Rep Robin',
            'checkamoun': 'CHECKAMOUN',
            'last_name': 'Last Name', # unused
            'first_name': 'First Name', # unused
            'credit_memo': 'Credit Memo',
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
                try:
                    customer_email = common.to_text(row['customer_email'])
                    customer = Customer.objects.filter(
                        email=customer_email).first()
                    if not customer:
                        continue
                except:
                    continue

            order, _ = Order.objects.get_or_create(
                order_no=order_no,
                defaults={
                    'customer': customer,
                    'order_date': common.to_date(row.get('order_date')),
                    'order_total': common.to_float(row.get('order_total')),
                    'terms': common.to_text(row.get('terms')),
                    'terms_due_date': common.to_date(row.get('terms_due_date')),
                    'order_code': common.to_text(row.get('order_code')),
                    'discount': common.to_float(row.get('discount')),
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
                    'check_number': common.to_text(row.get('check_number')),
                    'sales_rep_robin': row.get('sales_rep_robin') == True,
                    'checkamoun': common.to_float(row.get('checkamoun')),
                    'credit_memo': common.to_float(row.get('credit_memo')),
                    'additional_attributes': row.get('attributes')
                }
            )

            LineItem.objects.create(
                order=order,
                product=product,
                unit_price=common.to_float(row['unit_price']),
                quantity=common.to_int(row['quantity']),
                item_note=common.to_text(row['item_note']),
            )

    def company(self):

        Company.objects.all().delete()

        # Get Set Parts Data
        column_map = {
            'company_name': 'Company name',
            'company_note': 'Notes',

            'customer_no': 'Main Contact: Customer ID',
            'customer_email': 'Main Contact: Customer Email',

            'location_name': 'Location: Name',
            'location_note': 'Location: Notes',
            'location_phone': 'Location: Phone',
            'location_tax_exemption': 'Location: Tax Exemptions',
            'shipping_name': 'Location: Shipping Recipient',
            'shipping_phone': 'Location:ShippingPhone',
            'shipping_address1': 'Location: Shipping Address 1',
            'shipping_address2': 'Location: Shipping Address 2',
            'shipping_city': 'Location: Shipping City',
            'shipping_state': 'Location: Shipping Province Code',
            'shipping_zip': 'Location: Shipping Zip',
            'shipping_country': 'Location: Shipping Country Code',
            'billing_name': 'Location: Billing Recipient',
            'billing_phone': 'Location:BillingPhone',
            'billing_address1': 'Location: billing Address 1',
            'billing_address2': 'Location: Billing Address 2',
            'billing_city': 'Location: Billing City',
            'billing_state': 'Location: Billing Province Code',
            'billing_zip': 'Location: Billing Zip',
            'billing_country': 'Location: Billing Country Code',
        }

        rows = feed.readExcel(
            file_path=f"{FILEDIR}/wholesale-companies-master.xlsx",
            column_map=column_map,
            exclude=[]
        )

        # Set up Missing Customers
        for row in tqdm(rows):
            customer_no = common.to_text(row['customer_no'])
            customer_email = common.to_text(row['customer_email'])

            try:
                customer = Customer.objects.get(customer_no=customer_no)

                # if not customer.email and customer_email:
                #     customer.email = customer_email
                #     customer.save()

                # if customer_email:
                #     shopify_customer = shopify.update_customer(customer=customer)
                #     if shopify_customer:
                #         print(f"Updated customer {shopify_customer.id}")

                continue

            except Customer.DoesNotExist:
                pass

            shipping_first_name, shipping_last_name = common.to_name(row['shipping_name'])
            shipping_address1=common.to_text(row['shipping_address1'])
            shipping_address2=common.to_text(row['shipping_address2'])
            shipping_city=common.to_text(row['shipping_city'])
            shipping_state=common.to_text(row['shipping_state'])
            shipping_zip=common.to_text(row['shipping_zip'])
            shipping_country=common.to_text(row['shipping_country'])
            shipping_phone=common.to_phone(shipping_country, row['shipping_phone'])

            Customer.objects.create(
                customer_no=customer_no,
                email=customer_email,
                first_name=shipping_first_name,
                last_name=shipping_last_name,
                address1=shipping_address1,
                address2=shipping_address2,
                city=shipping_city,
                state=shipping_state,
                zip=shipping_zip,
                country=shipping_country,
                phone=shipping_phone,
            )

        # Read Orders
        for row in tqdm(rows):
            country=common.to_text(row['shipping_country'])

            company_name=common.to_text(row['company_name'])
            company_note=common.to_text(row['company_note'])
            location_name=common.to_text(row['location_name'])
            location_note=common.to_text(row['location_note'])
            location_phone=common.to_phone(country, row['location_phone'])
            location_tax_exemption=common.to_text(row['location_tax_exemption'])
            shipping_phone=common.to_phone(country, row['shipping_phone'])
            shipping_address1=common.to_text(row['shipping_address1'])
            shipping_address2=common.to_text(row['shipping_address2'])
            shipping_city=common.to_text(row['shipping_city'])
            shipping_state=common.to_text(row['shipping_state'])
            shipping_zip=common.to_text(row['shipping_zip'])
            shipping_country=common.to_text(row['shipping_country'])
            billing_phone=common.to_phone(country, row['billing_phone'])
            billing_address1=common.to_text(row['billing_address1'])
            billing_address2=common.to_text(row['billing_address2'])
            billing_city=common.to_text(row['billing_city'])
            billing_state=common.to_text(row['billing_state'])
            billing_zip=common.to_text(row['billing_zip'])
            billing_country=common.to_text(row['billing_country'])

            shipping_first_name, shipping_last_name = common.to_name(row['shipping_name'])

            billing_first_name, billing_last_name = common.to_name(row['billing_name'])

            customer_no = common.to_text(row['customer_no'])
            customer_email = common.to_text(row['customer_email'])

            try:
                customer = Customer.objects.get(
                    customer_no=customer_no)
            except Customer.DoesNotExist:
                print(f"Customer {customer_no} Not found")
                continue

            try:
                try:
                    Company.objects.get(company_name=company_name)
                    continue
                except Company.DoesNotExist:
                    pass

                Company.objects.create(
                    company_name=company_name,
                    company_note=company_note,

                    customer=customer,

                    location_name=location_name,
                    location_note=location_note,
                    location_phone=location_phone,
                    location_tax_exemption=location_tax_exemption,
                    shipping_phone=shipping_phone,
                    shipping_address1=shipping_address1,
                    shipping_address2=shipping_address2,
                    shipping_city=shipping_city,
                    shipping_state=shipping_state,
                    shipping_zip=shipping_zip,
                    shipping_country=shipping_country,
                    billing_phone=billing_phone,
                    billing_address1=billing_address1,
                    billing_address2=billing_address2,
                    billing_city=billing_city,
                    billing_state=billing_state,
                    billing_zip=billing_zip,
                    billing_country=billing_country,

                    shipping_first_name=shipping_first_name,
                    shipping_last_name=shipping_last_name,
                    billing_first_name=billing_first_name,
                    billing_last_name=billing_last_name,
                )

            except Exception as e:
                print(e)
                continue
