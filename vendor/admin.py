from django.contrib import admin

from .models import Vendor, Type, Collection, Tag, Product, Image


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    fields = [
        'name',
    ]

    list_display = [
        'name',
        'product_count'
    ]

    search_fields = [
        'name',
    ]


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    fields = [
        'name',
    ]

    list_display = [
        'name',
        'product_count'
    ]

    search_fields = [
        'name',
    ]


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    fields = [
        'name',
    ]

    list_display = [
        'name',
        'parent_count',
        'subcollection_count',
        'product_count',
    ]

    list_filter = [
        'parents',
    ]

    search_fields = [
        'name',
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = [
        'name',
    ]

    list_display = [
        'name',
        'product_count'
    ]

    search_fields = [
        'name',
    ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Primary', {'fields': [
            'sku',
            'title',
            'handle',
            'description',
            'barcode',
        ]}),
        ('Category', {'fields': [
            'vendor',
            'type',
            'collections',
            'tags',
        ]}),
        ('Pricing', {'fields': [
            'wholesale',
            'retail',
        ]}),
        ('Inventory & Shipping', {'fields': [
            'quantity',
            'weight',
        ]}),
        ("Status", {'fields': [
            'status',
        ]}),
        ("Attributes", {'fields': [
            'order_code',
            'attributes',
        ]}),
    ]

    list_display = [
        'sku',
        'title',
        'wholesale',
        'retail',
        'order_code',
        'status'
    ]

    list_filter = [
        'vendor',
        'type',
        'collections',
        'tags',
    ]

    search_fields = [
        'sku',
        'title',
        'handle',
        'description',
        'barcode',
        'attributes',
    ]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    autocomplete_fields = [
        'product',
    ]

    fields = [
        'path',
        'product',
    ]

    list_display = [
        'path',
        'product',
    ]

    list_filter = [
        'product__type__name',
        'product__collections__name',
    ]

    search_fields = [
        'path',
    ]
