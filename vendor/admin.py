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
        'product_count'
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
            'price',
            'compare',
            'cost',
        ]}),
        ('Inventory & Shipping', {'fields': [
            'quantity',
            'weight',
        ]}),
        ("Status", {'fields': [
            'status',
        ]}),
        ("Attriutes", {'fields': [
            'attriutes',
        ]}),
    ]

    list_display = [
        'sku',
        'title',
        'price',
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
        'attriutes',
    ]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    autocomplete_fields = [
        'product',
    ]

    fields = [
        'url',
        'product',
    ]

    list_display = [
        'url',
        'product',
    ]

    list_filter = [
        'product__type__name',
        'product__collections__name',
    ]

    search_fields = [
        'url',
    ]
