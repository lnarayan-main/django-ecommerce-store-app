from django.contrib import admin
from seller.models import Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'is_primary')
    readonly_fields = ('uploaded_at',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','description', 'category', 'price', 'stock', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'sku', 'brand')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
