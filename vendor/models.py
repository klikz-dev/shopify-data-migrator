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

    # Attributes
    parent_sku = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    category = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    length = models.FloatField(default=1, null=True, blank=True)
    height = models.FloatField(default=1, null=True, blank=True)
    country = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    order_code = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    dimensions = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    era = models.CharField(max_length=200, default=None, blank=True, null=True)
    circulation = models.CharField(
        max_length=200, default=None, blank=True, null=True)
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
    additional_attributes = models.JSONField(
        default=dict, blank=True, null=True)

    # Shopify
    product_id = models.CharField(
        max_length=200, default=None, blank=True, null=True)

    def __str__(self):
        return self.title


class Image(models.Model):
    path = models.URLField(max_length=1000, blank=False, null=False)
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.product.sku


class Setpart(models.Model):
    sku = models.CharField(max_length=200, primary_key=True)
    product = models.ForeignKey(
        Product, related_name="setparts", on_delete=models.CASCADE, blank=False, null=False)

    order_code = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    title = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    metal = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    diameter = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    circulation = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    assoc = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    price = models.FloatField(default=1, null=True, blank=True)
    obverse_detail = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    reverse_detail = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    country = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    unit_weight = models.FloatField(default=1, null=True, blank=True)

    def __str__(self):
        return self.product.sku
