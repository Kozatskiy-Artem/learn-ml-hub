from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import UserModel


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter password",
                "autocomplete": "new-password",
            }
        ),
        help_text="Your password must contain at least 8 characters.",
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm password",
                "autocomplete": "new-password",
            }
        ),
        help_text="Enter the same password as before, for verification.",
    )

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ["email", "password1", "password2", "first_name", "last_name"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter email"}),
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter first name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter last name"}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user = UserModel.objects.create_user(
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password1"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            is_active=True,
        )
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter email"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter password",
                "autocomplete": "current-password",
            }
        ),
    )


class UserUpdateForm(forms.Form):
    email = forms.EmailField(
        max_length=50,
        label="Електронна адреса:",
        required=False,
        disabled=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    avatar = forms.ImageField(
        label="Завантажте фото:",
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )
    first_name = forms.CharField(
        max_length=50,
        label="Введіть ім'я:",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ім'я"}),
    )
    last_name = forms.CharField(
        max_length=50,
        label="Введіть прізвище:",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Прізвище"}),
    )
