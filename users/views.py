from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from .forms import UserRegisterForm, UserUpdateForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            send_mail(
                subject="Добро пожаловать!",
                message="Спасибо за регистрацию в нашем магазине.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            login(request, user)
            return redirect("product_list")
    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", {"form": form})


@login_required
def profile_edit(request):
    if request.method == "POST":
        form = UserUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user,
        )
        if form.is_valid():
            form.save()
            return redirect("users:profile_edit")
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, "users/profile_edit.html", {"form": form})

