from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

User = get_user_model()


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "email",
            "phone",
            "avatar",
            "country",
            "password1",
            "password2",
        )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "phone", "avatar", "country")
