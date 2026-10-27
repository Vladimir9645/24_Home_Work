import os
from django import forms
from .models import Product

FORBIDDEN_WORDS = ["казино", "лотерея", "ставки", "бесплатно", "взятка"]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name:
            lower = name.lower()
            for word in FORBIDDEN_WORDS:
                if word in lower:
                    raise forms.ValidationError(f"В названии нельзя использовать слово «{word}».")
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if description:
            lower = description.lower()
            for word in FORBIDDEN_WORDS:
                if word in lower:
                    raise forms.ValidationError(f"В описании нельзя использовать слово «{word}».")
        return description

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return price

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            allowed_exts = [".jpg", ".jpeg", ".png"]
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in allowed_exts:
                raise forms.ValidationError("Разрешены только файлы JPG и PNG.")

            max_size_mb = 5
            max_size_bytes = max_size_mb * 1024 * 1024
            if image.size > max_size_bytes:
                raise forms.ValidationError(f"Размер изображения не должен превышать {max_size_mb} МБ.")
        return image

