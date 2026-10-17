# blog/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'blog/home.html')

def catalog(request):
    # Создаём пустой список — это валидное значение для переменной
    products = []
    # Передаём этот список в шаблон через контекст
    return render(request, 'blog/catalog.html', {'products': products})

