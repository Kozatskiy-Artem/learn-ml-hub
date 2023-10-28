from django import forms


class ImageUploadForm(forms.Form):
    title = forms.CharField(
        max_length=50,
        label="Введіть назву фото:",
        widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Назва фото"})
    )
    image = forms.ImageField(
        label="Завантажте фото:",
        widget=forms.FileInput(attrs={'class': 'form-control', "placeholder": "Оберіть фото", 'value': 'Вибрати фото',})
    )
