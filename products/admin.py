from django.contrib import admin
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}  # slug будет заполняться автоматически по названию

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_published", "owner", "category")
    list_filter = ("is_published", "category", "owner")
    search_fields = ("name", "description")
