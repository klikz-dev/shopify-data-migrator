import os
from shopify import Session as ShopifySession, Product as ShopifyProduct, Variant as ShopifyVariant, Image as ShopifyImage, SmartCollection as ShopifyCollection, InventoryLevel as ShopifyInventoryLevel

from utils import common

SHOPIFY_API_BASE_URL = os.getenv('SHOPIFY_API_BASE_URL')
SHOPIFY_API_VERSION = os.getenv('SHOPIFY_API_VERSION')
SHOPIFY_API_TOKEN = os.getenv('SHOPIFY_API_TOKEN')
SHOPIFY_API_THREAD_TOKENS = os.getenv('SHOPIFY_API_THREAD_TOKENS')


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
            'category',
            'length',
            'height',
            'country',
            'order_code',
            'dimensions',
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
            'product_attachment_file',
            'msrp',
            'additional_attributes'
        ]

        metafields = []
        for metafield_key in metafield_keys:
            metafield = {
                "namespace": "custom",
                "key": metafield_key,
                "value": getattr(product, metafield_key)
            }
            metafields.append(metafield)
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
        metafields = self.generate_product_metafields(product=product)
        product_tags = self.generate_product_tags(product=product)

        product_data = {
            "title": product.title.title(),
            "handle": common.to_handle(product.title),
            "body_html": product.description,
            "vendor": vendor,
            "product_type": product_type,
            "tags": product_tags,
            'metafields': metafields,
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
            'inventory_management': 'shopify',
            'fulfillment_service': 'manual',
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

    with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):

        shopify_product = ShopifyProduct()
        for key in product_data.keys():
            setattr(shopify_product, key, product_data.get(key))

        shopify_variant = ShopifyVariant()
        for key in variant_data.keys():
            setattr(shopify_variant, key, variant_data.get(key))
        shopify_product.variants = [shopify_variant]

        shopify_product.save()

        return shopify_product


def update_product(product, thread=None):

    processor = Processor(thread=thread)

    product_data = processor.generate_product_data(product=product)
    variant_data = processor.generate_variant_data(product=product)

    with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):

        shopify_product = ShopifyProduct.find(product.product_id)
        for key in product_data.keys():
            setattr(shopify_product, key, product_data.get(key))

        shopify_variant = ShopifyVariant()
        for key in variant_data.keys():
            setattr(shopify_variant, key, variant_data.get(key))
        shopify_product.variants = [shopify_variant]

        shopify_product.save()

        return shopify_product


def delete_product(id, thread=None):

    processor = Processor(thread=thread)

    with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):

        shopify_product = ShopifyProduct.find(id)
        success = shopify_product.destroy()

        return success


def upload_image(product_id, variant_id, position, src, alt, thread=None):

    processor = Processor(thread=thread)

    with ShopifySession.temp(SHOPIFY_API_BASE_URL, SHOPIFY_API_VERSION, processor.api_token):

        image_obj = {
            'product_id': product_id,
            'position': position,
            'src': src,
            'alt': alt,
        }
        if position % 10 == 1:
            image_obj['variant_ids'] = [variant_id]

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
