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
        'parents',
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
    class ImageInline(admin.StackedInline):
        model = Image
        extra = 0

        fields = [
            'path',
        ]

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
            'additional_attributes',
        ]}),
        ("Shopify", {'fields': [
            'product_id',
        ]}),
    ]

    list_display = [
        'sku',
        'title',
        'wholesale',
        'retail',
        'order_code',
        'status',
        'product_id',
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
        'additional_attributes',
    ]

    inlines = [ImageInline]


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
