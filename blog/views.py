from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from django.core.mail import send_mail
from django.conf import settings


# 1. СПИСОК СТАТЕЙ
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        # Возвращаем только опубликованные статьи, отсортированные по дате
        return Post.objects.filter(is_published=True).order_by('-created_at')



# 2. ПРОСМОТР СТАТЬИ
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)

        # КРИТЕРИЙ: Увеличение счетчика просмотров
        obj.views += 1
        obj.save(update_fields=['views'])

        # ДОП. ЗАДАНИЕ: Проверка на 100 просмотров
       # if obj.views == 100:
          #  self.send_congratulations_email(obj)

        return obj

    def send_congratulations_email(self, post):
        # Настройки почты должны быть в settings.py
        # Для теста можно использовать EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
        try:
            send_mail(
                subject=f'Поздравляем! Статья "{post.title}" набрала 100 просмотров!',
                message=f'Статья "{post.title}" достигла отметки в 100 просмотров.',
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@example.com'),
                recipient_list=[getattr(settings, 'ADMIN_EMAIL', 'admin@example.com')],
                fail_silently=False,
            )
        except Exception as e:
            # Если почта не настроена, просто пишем в консоль, чтобы сервер не упал
            print(f"Не удалось отправить письмо (настройте почту в settings.py): {e}")


# 3. СОЗДАНИЕ СТАТЬИ
class PostCreateView(CreateView):
    model = Post
    # Убедись, что эти поля точно есть в models.py
    fields = ['title', 'content', 'preview_image', 'is_published']
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')


# 4. РЕДАКТИРОВАНИЕ СТАТЬИ
class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content', 'preview_image', 'is_published']
    template_name = 'blog/post_form.html'

    # КРИТЕРИЙ: Редирект на страницу просмотра этой же статьи
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})


# 5. УДАЛЕНИЕ СТАТЬИ
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
