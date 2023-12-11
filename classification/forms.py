from django import forms


class ImageUploadForm(forms.Form):
    title = forms.CharField(
        max_length=50,
        label="Введіть назву фото:",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Назва фото"}),
    )
    image = forms.ImageField(
        label="Завантажте фото:",
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "placeholder": "Оберіть фото",
                "value": "Вибрати фото",
            }
        ),
    )


class HyperParamsForm(forms.Form):
    filters_1_layer = forms.IntegerField(
        min_value=1,
        max_value=128,
        label="Кількість фільтрів на першому згорткову шарі:",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    filters_2_layer = forms.IntegerField(
        min_value=1,
        max_value=128,
        label="Кількість фільтрів на другому згорткову шарі:",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    filters_3_layer = forms.IntegerField(
        min_value=1,
        max_value=128,
        label="Кількість фільтрів на третьому згорткову шарі:",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    dense_neurons = forms.IntegerField(
        min_value=1,
        max_value=1024,
        label="Кількість нейронів на повнозв'язаному шарі:",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    epochs = forms.IntegerField(
        min_value=1,
        max_value=20,
        label="Кількість епох навчання:",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
