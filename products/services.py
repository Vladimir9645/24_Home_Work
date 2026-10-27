from django.core.cache import cache
from .models import Product

CACHE_TIMEOUT = 300  # 5 минут

def get_product_cached(pk: int):
    cache_key = f"product_detail_{pk}"
    product = cache.get(cache_key)

    if product is None:
        product = Product.objects.get(pk=pk)
        cache.set(cache_key, product, CACHE_TIMEOUT)

    return product


def get_products_by_category_cached(category_slug: str):
    cache_key = f"products_by_category_{category_slug}"
    products = cache.get(cache_key)

    if products is None:
        products = list(
            Product.objects.filter(
                category__slug=category_slug,
                is_published=True
            )
        )
        cache.set(cache_key, products, CACHE_TIMEOUT)

    return products

def get_cached_products():
    """Кешированный список всех опубликованных товаров (для product_list)."""
    key = "product_list"
    products = cache.get(key)
    if products is not None:
        return products

    products = list(Product.objects.filter(is_published=True))
    cache.set(key, products, CACHE_TIMEOUT)
    return products


def invalidate_products_cache():
    """Сброс кеша общего списка товаров."""
    cache.delete("product_list")


def invalidate_product_cache(pk: int, category_slug: str | None = None):
    """Сброс кеша конкретного товара и списка по категории."""
    cache.delete(f"product_detail_{pk}")
    if category_slug:
        cache.delete(f"products_by_category_{category_slug}")
    invalidate_products_cache()
