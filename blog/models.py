from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Текст статьи')
    preview_image = models.ImageField('Превью', upload_to='posts/', blank=True, null=True)
    is_published = models.BooleanField('Опубликовано', default=False)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    views = models.PositiveIntegerField('Просмотры', default=0)

    class Meta:
        verbose_name = 'Статья блога'
        verbose_name_plural = 'Статьи блога'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

