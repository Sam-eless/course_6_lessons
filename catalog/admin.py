from django.contrib import admin

from catalog.models import Product, Category, Version


# Register your models here.

# admin.site.register(Product)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'purchase_price', 'category',)
    search_fields = ('name', 'purchase_price',)
    list_filter = ('category',)


# admin.site.register(Category)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('product', 'version_number', 'is_active')
