# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from blog.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    # path('', include('blog.urls')),       # если у блога есть главный роутинг
    path('products/', include('products.urls')),
    path('accounts/', include('users.urls')),  # подключаем пользователей
]

# Важно: отдаем медиа-файлы (аватары) в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
