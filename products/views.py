from django.shortcuts import get_object_or_404, render, redirect
from .models import Product
from .forms import ProductForm
from django.core.paginator import Paginator


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

def index(request):
    products = Product.objects.all().order_by('-created_at')
    paginator = Paginator(products, 6)  # 6 товаров на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'products/index.html', {'page_obj': page_obj})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})
