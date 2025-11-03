from django.contrib import admin
from seller.models import Product, ProductImage, Brand, Size, Color

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'is_primary')
    readonly_fields = ('uploaded_at',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','description', 'category', 'brand', 'price', 'stock', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'sku', 'brand')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'logo', 'created_at')
    search_fields = ('name',)
    # prepopulated_fields = {'slug': ('name',)}


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order')
    ordering = ('display_order',)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'hex_code')
    search_fields = ('name',)