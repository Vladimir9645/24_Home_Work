from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm


@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, "products/product_list.html", {"products": products})


@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            # Авто-привязка владельца
            product.owner = request.user
            product.save()
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
    product = get_object_or_404(Product, pk=pk)
    # Передаём флаги в шаблон, чтобы правильно показать кнопки
    is_owner = product.owner == request.user if product.owner else False
    is_moderator = request.user.groups.filter(name='Модератор продуктов').exists()
    can_unpublish = request.user.has_perm('products.can_unpublish_product')

    context = {
        "product": product,
        "is_owner": is_owner,
        "is_moderator": is_moderator,
        "can_unpublish": can_unpublish,
    }
    return render(request, "products/product_detail.html", context)


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Проверка прав: редактировать может только владелец или модератор
    is_owner = product.owner == request.user if product.owner else False
    is_moderator = request.user.groups.filter(name='Модератор продуктов').exists()

    if not (is_owner or is_moderator):
        # Можно вернуть 403 или просто редирект на список
        return redirect("product_list")

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
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

    # Проверка прав: удалять может только владелец или модератор
    is_owner = product.owner == request.user if product.owner else False
    is_moderator = request.user.groups.filter(name='Модератор продуктов').exists()

    if not (is_owner or is_moderator):
        return redirect("product_list")

    if request.method == "POST":
        product.delete()
        return redirect("product_list")

    return render(request, "products/product_confirm_delete.html", {"product": product})


@login_required
def unpublish_product(request, pk):
    """Снять товар с публикации — только для владельца или модератора с правом can_unpublish_product"""
    product = get_object_or_404(Product, pk=pk)

    is_owner = product.owner == request.user if product.owner else False
    is_moderator = request.user.groups.filter(name='Модератор продуктов').exists()
    can_unpublish = request.user.has_perm('products.can_unpublish_product')

    # Логика: владелец может снять с публикации всегда; модератор — только если у него есть право
    if not (is_owner or (is_moderator and can_unpublish)):
        return redirect("product_detail", pk=product.pk)

    product.is_published = False
    product.save()
    return redirect("product_detail", pk=product.pk)

