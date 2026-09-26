# products/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import ProductListView, ProductDetailView, ProductCreateView

urlpatterns = [
    # Пустая строка '' критически важна!
    path('', ProductListView.as_view(), name='index'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('add/', ProductCreateView.as_view(), name='add_product'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


