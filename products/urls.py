# products/urls.py
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

                  path("", views.product_list, name="product_list"),

                  path("create/", views.product_create, name="product_create"),
                  path("<int:pk>/", views.product_detail, name="product_detail"),
                  path("<int:pk>/edit/", views.product_edit, name="product_edit"),
                  path("<int:pk>/delete/", views.product_delete, name="product_delete"),

                  path('blog/', include('blog.urls', namespace='blog')),
                  path('users/', include('users.urls', namespace='users')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
