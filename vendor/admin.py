from django.contrib import admin

from .models import Vendor, Type, Collection, Tag, Product, Image, Setpart, Customer, Order, LineItem


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


@admin.register(Setpart)
class SetpartAdmin(admin.ModelAdmin):

    fields = [
        'sku',
        'order_code',
        'title',
        'parent_order_code',
        # 'metal',
        # 'diameter',
        # 'circulation',
        # 'assoc',
        # 'price',
        # 'obverse_detail',
        # 'reverse_detail',
        # 'info',
        # 'country',
        # 'unit_weight',
    ]

    list_display = [
        'sku',
        'order_code',
        'title',
        'parent_order_code',
    ]

    search_fields = [
        'sku',
        'order_code',
        'title',
        'parent_order_code',
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
            'add_box',
            'show_component',
            'track_qty',
        ]}),
        ("Attributes", {'fields': [
            'parent_sku',
            'length',
            'height',
            'country',
            'order_code',
            'dimensions',
            'denomination',
            'era',
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
            'binrr',
            'binother',
            'binmr',
            'bing',
            'notation',
            'bulk_qty',
            'additional_attributes',
        ]}),
        ("Variant", {'fields': [
            'variable',
            'circulation',
        ]}),
        ("Set Parts", {'fields': [
            'setparts',
        ]}),
        ("Shopify", {'fields': [
            'product_id',
            'variant_id',
        ]}),
    ]

    list_display = [
        'sku',
        'parent_sku',
        'title',
        'wholesale',
        'retail',
        'order_code',
        'variable',
        'circulation',
        'status',
        'product_id',
        'variant_id',
    ]

    list_filter = [
        'type__name',
        'status',
        'add_box',
        'show_component',
        'track_qty',
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
        'product_attachment_file',
        'msrp',
        'additional_attributes',
        'product_id',
        'variant_id',
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


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    # fields = [
    #     'customer_no',
    #     'email',
    #     'phone',
    #     'first_name',
    #     'last_name',
    #     'company',
    #     'address1',
    #     'address2',
    #     'city',
    #     'state',
    #     'zip',
    #     'country',
    #     'note',
    #     'tags',
    #     'type',
    #     'comm',
    #     'customer_id',
    # ]

    list_display = [
        'customer_no',
        'email',
        'phone',
        'first_name',
        'last_name',
        'address1',
        'city',
        'state',
        'zip',
        'country',
        'customer_id'
    ]

    list_filter = [
        'customer_type',
        'country',
        'tags'
    ]

    search_fields = [
        'customer_no',
        'email',
        'phone',
        'first_name',
        'last_name',
        'customer_id',
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    class LineItemInline(admin.StackedInline):
        model = LineItem
        extra = 0

        autocomplete_fields = [
            'product',
        ]

        fields = [
            'product',
            'unit_price',
            'quantity',
            'item_note',
        ]

    autocomplete_fields = [
        'customer',
    ]

    list_display = [
        'order_no',
        'customer',
        'shipping_cost',
        'shipping_method',
        'order_total',
        'amount_paid',
        'order_date',
        'order_id',
    ]

    list_filter = [
        'sales_rep_robin'
    ]

    search_fields = [
        'order_no',
        'shipping_method',
        'order_id',
    ]

    inlines = [LineItemInline]


@admin.register(LineItem)
class LineItemAdmin(admin.ModelAdmin):

    autocomplete_fields = [
        'order',
        'product',
    ]

    fields = [
        'order',
        'product',
        'unit_price',
        'quantity',
        'item_note'
    ]

    list_display = [
        'order',
        'product',
        'unit_price',
        'quantity',
        'item_note'
    ]
