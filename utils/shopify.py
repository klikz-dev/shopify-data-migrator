import os
import base64
import json
import requests
from pathlib import Path
from datetime import datetime
from shopify import GraphQL as ShopifyGraphQL, Session as ShopifySession, Product as ShopifyProduct, Variant as ShopifyVariant, Metafield as ShopifyMetafield, Image as ShopifyImage, SmartCollection as ShopifyCollection, InventoryLevel as ShopifyInventoryLevel, Customer as ShopifyCustomer, Order as ShopifyOrder, LineItem as ShopifyLineItem

from utils import common

SHOPIFY_API_BASE_URL = os.getenv('SHOPIFY_API_BASE_URL')
SHOPIFY_API_VERSION = os.getenv('SHOPIFY_API_VERSION')
SHOPIFY_API_TOKEN = os.getenv('SHOPIFY_API_TOKEN')
SHOPIFY_API_THREAD_TOKENS = os.getenv('SHOPIFY_API_THREAD_TOKENS')

FILEDIR = f"{Path(__file__).resolve().parent.parent}/vendor/management/files"


class Processor:
    def __init__(self, thread=None):

        self.api_token = SHOPIFY_API_TOKEN

        if thread != None:
            self.api_token = SHOPIFY_API_THREAD_TOKENS.split(",")[thread % 5]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def generate_product_metafields(self, product):
        metafield_keys = [
            'add_box',
            'show_component',
            'wholesale',
            'parent_sku',
            'length',
            'height',
            'country',
            'order_code',
            'dimensions',
            'denomination',
            'era',
            'circulation',
            'metal',
            'misc_product_info',
            'obverse_detail',
            'region',
            'reverse_detail',
            'ruler',
            'size',
            'subcategory',
            'custom_date',
            'news_from_date',
            'news_to_date',
            'msrp',
            'binrr',
            'binother',
            'binmr',
            'bing',
            'notation',
            'bulk_qty',
            'additional_attributes',
            'product_attachment_file'
        ]

        metafields = []
        for metafield_key in metafield_keys:
            metafield_value = getattr(product, metafield_key)

            if metafield_key == "product_attachment_file":
                file_path = f"{FILEDIR}/{metafield_value}"

                if file_path and os.path.isfile(file_path):
                    shopify_file = upload_file(
                        file_path=file_path,
                        file_type="application/pdf"
                    )

                    metafield = {
                        "namespace": "custom",
                        "key": metafield_key,
                        "value": shopify_file
                    }
                else:
                    continue
            else:
                if metafield_key == "additional_attributes":
                    metafield_value = json.dumps(metafield_value)

                metafield = {
                    "namespace": "custom",
                    "key": metafield_key,
                    "value": metafield_value
                }

            metafields.append(metafield)

        # Set Part
        setparts = []
        for setpart in product.setparts.all():
            setparts.append({
                'sku': setpart.sku,
                'order_code': setpart.order_code,
                'title': setpart.title,
                'parent_order_code': setpart.parent_order_code,
                # 'metal': setpart.metal,
                # 'diameter': setpart.diameter,
                # 'circulation': setpart.circulation,
                # 'assoc': setpart.assoc,
                # 'price': setpart.price,
                # 'obverse_detail': setpart.obverse_detail,
                # 'reverse_detail': setpart.reverse_detail,
                # 'info': setpart.info,
                # 'country': setpart.country,
                # 'unit_weight': setpart.unit_weight,
            })

        setpart_metafield = {
            "namespace": "custom",
            "key": 'setparts',
            "value": json.dumps(setparts),
        }
        metafields.append(setpart_metafield)
        # Set Part

        return metafields

    def generate_product_tags(self, product):

        tags = []

        collections = product.collections.all()

        for collection in collections:
            tags.append(f"Collection:{collection.name}")
            parent_collections = collection.parents.all()
            for parent_collection in parent_collections:
                tags.append(f"Collection:{parent_collection.name}")

        for tag in product.tags.all():
            tags.append(f"{tag.name}")

        return ",".join(tags)

    def generate_product_data(self, product):

        vendor = product.vendor.name
        product_type = product.type.name
        product_tags = self.generate_product_tags(product=product)

        # if len(product.setparts.all()) > 0:
        #     product_type = "Bundle"

        product_data = {
            "title": product.title.title(),
            "handle": common.to_handle(product.title),
            "body_html": product.description,
            "vendor": vendor,
            "product_type": product_type,
            "tags": product_tags,
        }

        if product_type == "Off Website" or not product.status:
            product_data['published_at'] = None

        return product_data

    def generate_variant_data(self, product, option=None):

        variant_data = {
            'price': product.retail,
            'sku': product.sku,
            'barcode': product.barcode,
            'weight': product.weight,
            'weight_unit': 'lb',
            'inventory_management': "shopify" if product.track_qty else None,
            'fulfillment_service': 'manual',
            'inventory_quantity': product.quantity,
            'taxable': False,
        }

        if option:
            variant_data['option1'] = option

        return variant_data


def list_products(thread=None):

    processor = Processor(thread=thread)

    with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):

        all_shopify_product_ids = []
        shopify_products = ShopifyProduct.find(limit=250)

        while shopify_products:

            print(f"Fetched {len(shopify_products)} Customers")

            for shopify_product in shopify_products:
                all_shopify_product_ids.append(shopify_product.id)

            shopify_products = shopify_products.has_next_page(
            ) and shopify_products.next_page() or []

        return all_shopify_product_ids


def get_product(id, thread=None):

    processor = Processor(thread=thread)

    with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):

        shopify_product = ShopifyProduct.find(id)

        return shopify_product


def create_product(product, thread=None):

    processor = Processor(thread=thread)

    product_data = processor.generate_product_data(product=product)
    variant_data = processor.generate_variant_data(product=product)
    metafields = processor.generate_product_metafields(product=product)

    with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):

        shopify_product = ShopifyProduct()
        for key in product_data.keys():
            setattr(shopify_product, key, product_data.get(key))

        shopify_variant = ShopifyVariant()
        for key in variant_data.keys():
            setattr(shopify_variant, key, variant_data.get(key))
        shopify_product.variants = [shopify_variant]

        if shopify_product.save():

            for metafield in metafields:
                shopify_metafield = ShopifyMetafield()
                shopify_metafield.namespace = metafield['namespace']
                shopify_metafield.key = metafield['key']
                shopify_metafield.value = metafield['value']
                shopify_product.add_metafield(shopify_metafield)

        else:
            print(shopify_product.errors.full_messages())

        return shopify_product


def create_variable_product(product, variants, thread=None):

    processor = Processor(thread=thread)

    first_variant = variants.first()

    metafields = processor.generate_product_metafields(product=product)

    with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):

        shopify_product = ShopifyProduct.find(product.product_id)
        shopify_product.product_type = "Variable"
        shopify_product.options = [{"name": first_variant.variable.title()}]

        shopify_variants = []
        for variant in variants:
            variant_data = processor.generate_variant_data(
                product=variant, option=variant.circulation)
            shopify_variant = ShopifyVariant()
            for key in variant_data.keys():
                setattr(shopify_variant, key, variant_data.get(key))
            shopify_variants.append(shopify_variant)

        shopify_product.variants = shopify_variants

        if shopify_product.save():

            for metafield in metafields:
                shopify_metafield = ShopifyMetafield()
                shopify_metafield.namespace = metafield['namespace']
                shopify_metafield.key = metafield['key']
                shopify_metafield.value = metafield['value']
                shopify_product.add_metafield(shopify_metafield)

            for variant in shopify_product.variants:
                if variant.option1.lower() == "default title":
                    try:
                        variant.destroy()
                        print(
                            f"Deleted variant with ID {variant.id} and title 'default title'")
                    except Exception as e:
                        print(
                            f"Failed to delete variant with ID {variant.id}: {str(e)}")

        else:
            print(shopify_product.errors.full_messages())

        return shopify_product


def update_product(product, thread=None):

    processor = Processor(thread=thread)

    product_data = processor.generate_product_data(product=product)
    # variant_data = processor.generate_variant_data(product=product)
    # metafields = processor.generate_product_metafields(product=product)

    with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):

        shopify_product = ShopifyProduct.find(product.product_id)
        for key in product_data.keys():
            setattr(shopify_product, key, product_data.get(key))

        # shopify_variant = ShopifyVariant()
        # for key in variant_data.keys():
        #     setattr(shopify_variant, key, variant_data.get(key))
        # shopify_product.variants = [shopify_variant]

        shopify_product.save()

        # for metafield in metafields:
        #     shopify_metafield = ShopifyMetafield()
        #     shopify_metafield.namespace = metafield['namespace']
        #     shopify_metafield.key = metafield['key']
        #     shopify_metafield.value = metafield['value']

        #     if metafield['key'] == "setparts":
        #         shopify_metafield.type_type = 'json_string'

        #     shopify_metafield.save()

        #     shopify_product.add_metafield(shopify_metafield)

        return shopify_product


def delete_product(id, thread=None):

    processor = Processor(thread=thread)

    with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):

        shopify_product = ShopifyProduct.find(id)
        success = shopify_product.destroy()

        return success


def upload_image(product_id, image, alt, thread=None):

    processor = Processor(thread=thread)

    with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):

        with open(image, "rb") as image_file:
            encoded_string = base64.b64encode(
                image_file.read()).decode('utf-8')

            image_obj = {
                'product_id': product_id,
                'attachment': encoded_string,
                'filename': os.path.basename(image),
                'alt': alt,
                'position': thread,
            }

            shopify_image = ShopifyImage(image_obj)
            shopify_image.save()

            return shopify_image


def delete_image(product_id, image_id, thread=None):

    processor = Processor(thread=thread)

    with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):

        shopify_product = ShopifyProduct.find(product_id)

        image_to_delete = None
        for shopify_image in shopify_product.images:

            if str(shopify_image.id) == str(image_id):
                image_to_delete = shopify_image
                break

        if image_to_delete:
            image_to_delete.destroy()

        return True


def upload_file(file_path, file_type, thread=None):
    processor = Processor(thread=thread)

    with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):
        shopifyGraphQL = ShopifyGraphQL()

        try:
            # Perform staged upload
            mutation = """
                mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
                    stagedUploadsCreate(input: $input) {
                        stagedTargets {
                            url
                            parameters {
                                name
                                value
                            }
                        }
                        userErrors {
                            field
                            message
                        }
                    }
                }
            """
            variables = {
                'input': [
                    {
                        'resource': "FILE",
                        'filename': os.path.basename(file_path),
                        'mimeType': file_type,
                        "httpMethod": "POST",
                    }
                ]
            }
            response = shopifyGraphQL.execute(mutation, variables=variables)
            response_data = json.loads(response)

            staged_targets = response_data.get('data', {}).get(
                'stagedUploadsCreate', {}).get('stagedTargets', [])
            upload_url = staged_targets[0]['url']
            upload_parameters = staged_targets[0]['parameters']

            upload_data = {param['name']: param['value']
                           for param in upload_parameters}

            # Upload the file
            with open(file_path, 'rb') as f:
                response = requests.post(
                    upload_url, data=upload_data, files={'file': f})

            uploaded_file_url = upload_data['key']

            # Create file object in Shopify
            mutation = """
                mutation fileCreate($files: [FileCreateInput!]!) {
                    fileCreate(files: $files) {
                        files {
                            id
                            fileStatus
                            preview {
                                image {
                                    url
                                }
                            }
                            createdAt
                        }
                    }
                }
            """
            variables = {
                "files": [
                    {
                        "contentType": "FILE",
                        "originalSource": f"https://storage.googleapis.com/shopify-staged-uploads/{uploaded_file_url}"
                    }
                ]
            }
            response = shopifyGraphQL.execute(
                mutation, variables=variables)
            response_data = json.loads(response)

            file_id = response_data['data']['fileCreate']['files'][0]['id']
            return file_id

        except Exception as e:
            print(e)
            return None


def list_collections(thread=None):

    processor = Processor(thread=thread)

    with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):

        all_shopify_collections = []
        shopify_collections = ShopifyCollection.find(limit=250)

        while shopify_collections:

            all_shopify_collections.extend(shopify_collections)

            shopify_collections = shopify_collections.has_next_page(
            ) and shopify_collections.next_page() or []

        return all_shopify_collections


def get_collection(id, thread=None):

    processor = Processor(thread=thread)

    with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):

        shopify_collection = ShopifyCollection.find(id)

        return shopify_collection


def create_collection(title, rules, thread=None):

    processor = Processor(thread=thread)

    with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):

        shopify_collection = ShopifyCollection()

        shopify_collection.title = title
        shopify_collection.rules = rules
        shopify_collection.save()

        return shopify_collection


def update_collection(id, title, rules, thread=None):

    processor = Processor(thread=thread)

    with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):

        shopify_collection = ShopifyCollection.find(id)

        shopify_collection.title = title
        shopify_collection.rules = rules
        shopify_collection.save()

        return shopify_collection


def delete_collection(id, thread=None):

    processor = Processor(thread=thread)

    with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):

        shopify_collection = ShopifyCollection.find(id)

        success = shopify_collection.destroy()

        return success


def update_inventory(inventory, thread=None):

    processor = Processor(thread=thread)

    with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):

        shopify_variant = ShopifyVariant.find(inventory.variant.id)
        inventory_item_id = shopify_variant.inventory_item_id

        inventory_levels = ShopifyInventoryLevel.find(
            inventory_item_ids=inventory_item_id, location_ids='66503311469')

        if inventory_levels:
            inventory_level = inventory_levels[0]
            inventory_level.set(location_id='66503311469',
                                inventory_item_id=inventory_item_id, available=inventory.quantity)

            return inventory_level

        else:
            return None


def list_customers(thread=None):

    processor = Processor(thread=thread)

    with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):

        all_shopify_customer_ids = []
        shopify_customers = ShopifyCustomer.find(limit=250)

        while shopify_customers:

            print(f"Fetched {len(shopify_customers)} Customers")

            for shopify_customer in shopify_customers:
                all_shopify_customer_ids.append(shopify_customer.id)

            shopify_customers = shopify_customers.has_next_page(
            ) and shopify_customers.next_page() or []

        return all_shopify_customer_ids


def create_customer(customer, thread=None):
    processor = Processor(thread=thread)

    with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):

        customer_data = {
            "email": customer.email,
            "phone": customer.phone,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "addresses": [
                {
                    "address1": customer.address1,
                    "city": customer.city,
                    "province": customer.state,
                    "country": customer.country,
                    "zip": customer.zip,
                    "last_name": customer.last_name,
                    "first_name": customer.first_name,
                    "phone": customer.phone,
                    "company": customer.company,
                }
            ],
            "note": customer.note,
            "tags": customer.tags,
        }

        shopify_customer = ShopifyCustomer(customer_data)

        if shopify_customer.save():

            metafield_data = {
                "namespace": "custom",
                "key": "customer_",
                "value": customer.customer_no
            }
            shopify_metafield = ShopifyMetafield(metafield_data)
            shopify_customer.add_metafield(shopify_metafield)

            metafield_data = {
                "namespace": "custom",
                "key": "customer_type",
                "value": customer.type
            }
            shopify_metafield = ShopifyMetafield(metafield_data)
            shopify_customer.add_metafield(shopify_metafield)

            metafield_data = {
                "namespace": "custom",
                "key": "trade_show_sales_representative",
                "value": customer.comm
            }
            shopify_metafield = ShopifyMetafield(metafield_data)
            shopify_customer.add_metafield(shopify_metafield)

        elif customer.email:

            print(shopify_customer.errors.full_messages())

            del customer_data['phone']
            for address in customer_data["addresses"]:
                if 'phone' in address:
                    del address['phone']

            shopify_customer = ShopifyCustomer(customer_data)
            if shopify_customer.save():

                metafield_data = {
                    "namespace": "custom",
                    "key": "customer_",
                    "value": customer.customer_no
                }
                shopify_metafield = ShopifyMetafield(metafield_data)
                shopify_customer.add_metafield(shopify_metafield)

                metafield_data = {
                    "namespace": "custom",
                    "key": "customer_type",
                    "value": customer.type
                }
                shopify_metafield = ShopifyMetafield(metafield_data)
                shopify_customer.add_metafield(shopify_metafield)

                metafield_data = {
                    "namespace": "custom",
                    "key": "trade_show_sales_representative",
                    "value": customer.comm
                }
                shopify_metafield = ShopifyMetafield(metafield_data)
                shopify_customer.add_metafield(shopify_metafield)

            else:
                print(shopify_customer.errors.full_messages())

        return shopify_customer


def update_customer(customer, thread=None):
    processor = Processor(thread=thread)

    with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):

        shopify_customer = ShopifyCustomer.find(customer.customer_id)

        shopify_customer.email = customer.email
        shopify_customer.phone = customer.phone
        shopify_customer.first_name = customer.first_name
        shopify_customer.last_name = customer.last_name
        shopify_customer.note = customer.note
        shopify_customer.tags = customer.tags

        if shopify_customer.save():

            metafield_data = {
                "namespace": "custom",
                "key": "customer_",
                "value": customer.customer_no
            }
            shopify_metafield = ShopifyMetafield(metafield_data)
            shopify_customer.add_metafield(shopify_metafield)

            metafield_data = {
                "namespace": "custom",
                "key": "customer_type",
                "value": customer.type
            }
            shopify_metafield = ShopifyMetafield(metafield_data)
            shopify_customer.add_metafield(shopify_metafield)

            metafield_data = {
                "namespace": "custom",
                "key": "trade_show_sales_representative",
                "value": customer.comm
            }
            shopify_metafield = ShopifyMetafield(metafield_data)
            shopify_customer.add_metafield(shopify_metafield)

        return shopify_customer


def delete_customer(id, thread=None):

    processor = Processor(thread=thread)

    with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):

        shopify_customer = ShopifyCustomer.find(id)

        success = shopify_customer.destroy()

        return success


def list_orders(thread=None):

    processor = Processor(thread=thread)

    with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):

        all_shopify_order_ids = []
        shopify_orders = ShopifyOrder.find(limit=250, status="any")

        while shopify_orders:

            print(f"Fetched {len(shopify_orders)} Orders.")

            for shopify_order in shopify_orders:
                all_shopify_order_ids.append(shopify_order.id)

            shopify_orders = shopify_orders.has_next_page(
            ) and shopify_orders.next_page() or []

            if len(all_shopify_order_ids) > 5000:
                break

        return all_shopify_order_ids


def create_order(order, thread=None):
    processor = Processor(thread=thread)

    with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):

        shopify_order = ShopifyOrder()
        # if order.customer.email:
        #     shopify_order.email = order.customer.email
        # if order.customer.phone:
        #     shopify_order.phone = order.customer.phone

        shopify_order.order_number = order.order_no

        shopify_order.customer = {
            "id": order.customer.customer_id
        }

        line_items = []
        for item in order.lineItems.all():
            try:
                shopify_product = ShopifyProduct.find(item.product.product_id)
                variant_id = shopify_product.variants[0].id
            except:
                continue

            line_item = ShopifyLineItem({
                "variant_id": variant_id,
                "title": item.product.title,
                "quantity": item.quantity if item.quantity >= 1 else 1,
                "price": item.unit_price
            })
            line_items.append(line_item)

        shopify_order.line_items = line_items

        shopify_order.total_price = order.total
        shopify_order.shipping_lines = [{
            "title": order.shipping_method,
            "code": order.shipping_method,
            "price": order.shipping
        }]

        if order.order_date:
            shopify_order.created_at = order.order_date.isoformat()
        shopify_order.fulfillment_status = "fulfilled"

        if shopify_order.save():
            metafield_data = {
                "namespace": "custom",
                "key": "original_order_id",
                "value": order.order_no
            }
            shopify_metafield = ShopifyMetafield(metafield_data)
            shopify_order.add_metafield(shopify_metafield)
        else:
            print(shopify_order.errors.full_messages())

        return shopify_order


def update_order(order, thread=None):
    processor = Processor(thread=thread)

    with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):

        shopify_order = ShopifyOrder.find(order.order_id)
        shopify_order.customer = order.customer
        shopify_order.line_items = [ShopifyLineItem({
            "product_id": item.product.product_id,
            "quantity": item.quantity,
            "price": item.unit_price
        }) for item in order.lineItems.all()]
        shopify_order.created_at = order.order_date

        shopify_order.save()

        return shopify_order


def delete_order(id, thread=None):

    processor = Processor(thread=thread)

    with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):

        shopify_order = ShopifyOrder.find(id)

        success = shopify_order.destroy()

        return success
