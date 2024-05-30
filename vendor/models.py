from django.db import models


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
        return self.products.count()

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
    order_code = models.CharField(
        max_length=200, default=None, blank=True, null=True)
    attributes = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return self.title


class Image(models.Model):
    path = models.URLField(max_length=1000, blank=False, null=False)
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.product.sku
