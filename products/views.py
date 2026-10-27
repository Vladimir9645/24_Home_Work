from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .services import get_product_cached, get_products_by_category_cached, invalidate_product_cache
from .models import Product
from .forms import ProductForm


@login_required
def product_list(request):
    # Используем свой кеш вместо Product.objects.all()
    from .services import get_cached_products  # нужно добавить эту функцию в services.py (см. ниже)
    products = get_cached_products()
    return render(request, "products/product_list.html", {"products": products})


@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            # Сбрасываем кеш списков, чтобы новый товар сразу появился
            from .services import invalidate_products_cache
            invalidate_products_cache()
            return redirect("product_list")
    else:
        form = ProductForm()

    return render(
        request,
        "products/product_form.html",
        {"form": form, "title": "Добавить товар"},
    )


@login_required
def product_detail(request, pk):
    product = get_product_cached(pk)
    return render(request, "products/product_detail.html", {"product": product})


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    is_owner = product.owner == request.user if product.owner else False
    is_moderator = request.user.groups.filter(name='Модератор продуктов').exists()

    if not (is_owner or is_moderator):
        return redirect("product_list")

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            # сбрасываем кеш после сохранения
            category_slug = product.category.slug if product.category else None
            invalidate_product_cache(product.pk, category_slug)
            return redirect("product_detail", pk=product.pk)
    else:
        form = ProductForm(instance=product)

    return render(
        request,
        "products/product_form.html",
        {"form": form, "title": "Редактировать товар", "product": product},
    )


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    is_owner = product.owner == request.user if product.owner else False
    is_moderator = request.user.groups.filter(name='Модератор продуктов').exists()

    if not (is_owner or is_moderator):
        return redirect("product_list")

    if request.method == "POST":
        category_slug = product.category.slug if product.category else None
        # Сначала сбрасываем кеш, потом удаляем
        invalidate_product_cache(product.pk, category_slug)
        product.delete()
        return redirect("product_list")

    return render(request, "products/product_confirm_delete.html", {"product": product})


@login_required
def unpublish_product(request, pk):
    """Снять товар с публикации — владелец ИЛИ модератор с правом can_unpublish_product ИЛИ суперюзер"""
    product = get_object_or_404(Product, pk=pk)

    is_owner = product.owner == request.user if product.owner else False
    is_moderator = request.user.groups.filter(name='Модератор продуктов').exists()
    can_unpublish = request.user.has_perm('products.can_unpublish_product')

    if not (is_owner or (is_moderator and can_unpublish) or request.user.is_staff):
        return redirect("product_detail", pk=product.pk)

    product.is_published = False
    product.save(update_fields=['is_published'])

    category_slug = product.category.slug if product.category else None
    invalidate_product_cache(product.pk, category_slug)
    return redirect("product_detail", pk=product.pk)


@login_required
def products_by_category(request, category_slug):
    products = get_products_by_category_cached(category_slug)
    return render(
        request,
        "products/products_by_category.html",
        {"products": products, "category_slug": category_slug},
    )
