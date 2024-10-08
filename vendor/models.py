from django.db import models
from django.db.models import Count, Q


class Vendor(models.Model):
    name = models.CharField(max_length=200, primary_key=True)

    def product_count(self):
        return self.products.count()

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=200, primary_key=True)

    def product_count(self):
        return self.products.count()

    def __str__(self):
        return self.name


class Collection(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    parents = models.ManyToManyField(
        'self', symmetrical=False, related_name='subcollections', blank=True)

    def parent_count(self):
        return self.parents.count()

    def subcollection_count(self):
        return self.subcollections.count()

    def product_count(self):
        products = Product.objects.filter(
            Q(collections=self) | Q(collections__parents=self))
        return products.distinct().count()

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, primary_key=True)

    def product_count(self):
        return self.products.count()

    def __str__(self):
        return self.name


class Setpart(models.Model):
    sku = models.CharField(max_length=200, primary_key=True)
    order_code = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    title = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    parent_order_code = models.CharField(
        max_length=200, default=None, blank=True, null=True)

    def __str__(self):
        return self.sku


class Product(models.Model):
    # Primary
    sku = models.CharField(max_length=200, primary_key=True)
    title = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    handle = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    description = models.TextField(
        max_length=5000, default=None, blank=True, null=True)
    barcode = models.CharField(
        max_length=200, default=None, blank=True, null=True)

    # Category
    vendor = models.ForeignKey(
        Vendor, related_name="products", on_delete=models.CASCADE, blank=False, null=False)
    type = models.ForeignKey(
        Type, related_name="products", on_delete=models.CASCADE, blank=False, null=False)
    collections = models.ManyToManyField(Collection, related_name="products")
    tags = models.ManyToManyField(Tag, related_name="products")

    # Pricing
    wholesale = models.FloatField(default=0, blank=False, null=False)
    retail = models.FloatField(default=0, blank=True, null=True)

    # Inventory & Shipping
    quantity = models.IntegerField(default=0, null=True, blank=True)
    weight = models.FloatField(default=1, null=True, blank=True)

    # Status
    status = models.BooleanField(default=True)
    add_box = models.BooleanField(default=True)
    show_component = models.BooleanField(default=True)
    track_qty = models.BooleanField(default=True)

    # Attributes
    parent_sku = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    length = models.FloatField(default=1, null=True, blank=True)
    height = models.FloatField(default=1, null=True, blank=True)
    country = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    order_code = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    dimensions = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    denomination = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    era = models.CharField(max_length=200, default=None, blank=True, null=True)
    metal = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    misc_product_info = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    obverse_detail = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    region = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    reverse_detail = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    ruler = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    size = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    subcategory = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    custom_date = models.DateField(default=None, blank=True, null=True)
    news_from_date = models.DateField(default=None, blank=True, null=True)
    news_to_date = models.DateField(default=None, blank=True, null=True)
    product_attachment_file = models.CharField(
        max_length=2000, default=None, blank=True, null=True)
    msrp = models.FloatField(default=1, null=True, blank=True)
    binrr = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    binother = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    binmr = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    bing = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    notation = models.TextField(
        max_length=2000, default=None, null=True, blank=True)

    assoc = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    slvrcont = models.FloatField(default=0, null=True, blank=True)
    unit_weight = models.FloatField(default=0, null=True, blank=True)
    slvweight = models.FloatField(default=0, null=True, blank=True)
    txtsilveryr = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    centurytxt = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    chksilver = models.BooleanField(default=False)
    invhdate = models.DateField(null=True, blank=True)

    bulk_qty = models.IntegerField(default=0, null=True, blank=True)
    additional_attributes = models.JSONField(
        default=dict, blank=True, null=True)

    call_for_price = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0, null=True, blank=True)
    keywords = models.CharField(
        max_length=500, default=None, null=True, blank=True)
    seo_title = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    meta_description = models.CharField(
        max_length=1000, default=None, null=True, blank=True)

    # Variant
    variable = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    circulation = models.CharField(
        max_length=200, default=None, blank=True, null=True)

    # Set Parts
    setparts = models.ManyToManyField(
        Setpart, related_name="products", blank=True)

    # Shopify
    product_id = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    # Shopify
    variant_id = models.CharField(
        max_length=200, default=None, blank=True, null=True)

    def __str__(self):
        return self.title


class Image(models.Model):
    path = models.CharField(
        max_length=2000, default=None, blank=False, null=False)
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.product.sku


class Customer(models.Model):

    customer_no = models.CharField(max_length=200, primary_key=True)

    email = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    phone = models.CharField(
        max_length=200, default=None, null=True, blank=True)

    first_name = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    last_name = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    company = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    address1 = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    address2 = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    city = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    state = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    zip = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    country = models.CharField(
        max_length=200, default=None, null=True, blank=True)

    note = models.TextField(
        max_length=2000, default=None, null=True, blank=True)
    tags = models.CharField(
        max_length=200, default=None, null=True, blank=True)

    customer_type = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    trade_show_sales_representative = models.BooleanField(default=False)
    payment_terms = models.IntegerField(default=None, null=True, blank=True)
    vat_no = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    orig_ad = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    check_dropship = models.BooleanField(default=False)
    additional_attributes = models.JSONField(
        default=dict, blank=True, null=True)

    customer_id = models.CharField(
        max_length=200, default=None, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Company(models.Model):
    company_name = models.CharField(max_length=200, primary_key=True)
    company_note = models.CharField(
        max_length=200, default=None, null=True, blank=True)

    customer = models.ForeignKey(
        Customer, related_name='companies', on_delete=models.CASCADE, blank=False, null=False)

    location_name = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    location_note = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    location_phone = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    location_tax_exemption = models.CharField(
        max_length=200, default=None, null=True, blank=True)

    shipping_first_name = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    shipping_last_name = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    shipping_phone = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    shipping_address1 = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    shipping_address2 = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    shipping_city = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    shipping_state = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    shipping_zip = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    shipping_country = models.CharField(
        max_length=200, default=None, null=True, blank=True)

    billing_first_name = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    billing_last_name = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    billing_phone = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    billing_address1 = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    billing_address2 = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    billing_city = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    billing_state = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    billing_zip = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    billing_country = models.CharField(
        max_length=200, default=None, null=True, blank=True)

    company_id = models.CharField(
        max_length=200, default=None, null=True, blank=True)

    def __str__(self):
        return f"{self.company_name}"


class Order(models.Model):

    order_no = models.CharField(max_length=200, primary_key=True)

    customer = models.ForeignKey(
        Customer, related_name='orders', on_delete=models.CASCADE, blank=False, null=False)

    order_total = models.FloatField(default=0, null=False, blank=False)
    order_date = models.DateField(null=True, blank=True)
    terms = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    terms_due_date = models.DateField(null=True, blank=True)
    order_code = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    discount = models.FloatField(default=0, null=False, blank=False)
    payment_method = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    card_type = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    approval = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    shipping_method = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    shipping_cost = models.FloatField(default=0, null=False, blank=False)
    order_memo = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    customer_no = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    company = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    amount_paid = models.FloatField(default=0, null=False, blank=False)
    po_number = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    tracking_number = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    sales_rep_robin = models.BooleanField(default=False)
    check_number = models.CharField(
        max_length=200, default=None, null=True, blank=True)
    checkamoun = models.FloatField(default=0, null=True, blank=True)
    credit_memo = models.FloatField(default=0, null=True, blank=True)
    additional_attributes = models.JSONField(
        default=dict, blank=True, null=True)

    order_id = models.CharField(
        max_length=200, default=None, null=True, blank=True)

    def __str__(self):
        return self.order_no


class LineItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='lineItems', on_delete=models.CASCADE, blank=False, null=False)

    product = models.ForeignKey(
        Product, related_name='lineItems', on_delete=models.CASCADE, blank=False, null=False)

    unit_price = models.FloatField(default=0, null=False, blank=False)

    quantity = models.IntegerField(default=1, null=False, blank=False)

    item_note = models.CharField(
        max_length=200, default=None, null=True, blank=True)

    def __str__(self):
        return self.order.order_no
