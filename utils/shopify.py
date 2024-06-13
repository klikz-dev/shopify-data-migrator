import os
import base64
import json
import requests
from pathlib import Path
from shopify import GraphQL as ShopifyGraphQL, Session as ShopifySession, Product as ShopifyProduct, Variant as ShopifyVariant, Metafield as ShopifyMetafield, Image as ShopifyImage, SmartCollection as ShopifyCollection, InventoryLevel as ShopifyInventoryLevel

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
            'retail',
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
                'parent_order_code': setpart.parent_order_code,
                'order_code': setpart.order_code,
                'title': setpart.title,
                'metal': setpart.metal,
                'diameter': setpart.diameter,
                'circulation': setpart.circulation,
                'assoc': setpart.assoc,
                'price': setpart.price,
                'obverse_detail': setpart.obverse_detail,
                'reverse_detail': setpart.reverse_detail,
                'info': setpart.info,
                'country': setpart.country,
                'unit_weight': setpart.unit_weight,
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

        for tag in product.tags.all():
            tags.append(f"{tag.name}")

        return ",".join(tags)

    def generate_product_data(self, product):

        vendor = product.vendor.name
        product_type = product.type.name
        product_tags = self.generate_product_tags(product=product)

        product_data = {
            "title": product.title.title(),
            "handle": common.to_handle(product.title),
            "body_html": product.description,
            "vendor": vendor,
            "product_type": product_type,
            "tags": product_tags,
        }

        return product_data

    def generate_variant_data(self, product):

        variant_data = {
            'price': product.wholesale,
            'sku': product.sku,
            'barcode': product.barcode,
            'weight': product.weight,
            'weight_unit': 'lb',
            'inventory_quantity': product.quantity,
            'inventory_management': None,
            'fulfillment_service': 'manual',
            'taxable': False,
        }

        return variant_data


def list_products(thread=None):

    processor = Processor(thread=thread)

    with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):

        all_shopify_products = []
        shopify_products = ShopifyProduct.find(limit=250)

        while shopify_products:

            all_shopify_products.extend(shopify_products)

            shopify_products = shopify_products.has_next_page(
            ) and shopify_products.next_page() or []

        return all_shopify_products


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

        shopify_product.save()

        for metafield in metafields:
            shopify_metafield = ShopifyMetafield()
            shopify_metafield.namespace = metafield['namespace']
            shopify_metafield.key = metafield['key']
            shopify_metafield.value = metafield['value']
            shopify_product.add_metafield(shopify_metafield)

        return shopify_product


def update_product(product, thread=None):

    processor = Processor(thread=thread)

    product_data = processor.generate_product_data(product=product)
    variant_data = processor.generate_variant_data(product=product)
    metafields = processor.generate_product_metafields(product=product)

    with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):

        shopify_product = ShopifyProduct.find(product.product_id)
        for key in product_data.keys():
            setattr(shopify_product, key, product_data.get(key))

        shopify_variant = ShopifyVariant()
        for key in variant_data.keys():
            setattr(shopify_variant, key, variant_data.get(key))
        shopify_product.variants = [shopify_variant]

        shopify_product.save()

        for metafield in metafields:
            shopify_metafield = ShopifyMetafield()
            shopify_metafield.namespace = metafield['namespace']
            shopify_metafield.key = metafield['key']
            shopify_metafield.value = metafield['value']

            if metafield['key'] == "setparts":
                shopify_metafield.type_type = 'json_string'

            shopify_metafield.save()

            shopify_product.add_metafield(shopify_metafield)

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
            inventory_item_ids=inventory_item_id, location_ids='97762935103')

        if inventory_levels:
            inventory_level = inventory_levels[0]
            inventory_level.set(location_id='97762935103',
                                inventory_item_id=inventory_item_id, available=inventory.quantity)

            return inventory_level

        else:
            return None
