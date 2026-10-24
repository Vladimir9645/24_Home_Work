from django.contrib import admin
from .models import Article  # замени Article на имя своей модели статьи

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'views')
    list_filter = ('status',)
    search_fields = ('title',)
