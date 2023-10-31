from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from core.containers import ServiceContainer
from core.exceptions import InstanceNotExistError

from .forms import LoginForm, RegisterForm


def registration(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, "info_pages/home.html")
        else:
            context = {"form": form}
            return render(request, "auth/registration.html", context)
    else:
        if request.user.is_authenticated:
            return redirect("/")
        form = RegisterForm()
        context = {"form": form}
        return render(request, "auth/registration.html", context)


def log_in(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.data["email"]
            password = form.data["password"]
            user = authenticate(request, email=email, password=password)
            if user and user.check_password(password):
                login(request, user)
                if request.GET.get("next"):
                    return redirect(request.GET.get("next"))
                return redirect("/")
        context = {"error_message": "Invalid login credentials", "form": form}
        return render(request, "auth/login.html", context)
    else:
        if request.user.is_authenticated:
            return redirect("/")
        form = LoginForm()
        context = {"form": form}
        return render(request, "auth/login.html", context)


@login_required
def log_out(request):
    if request.method == "POST":
        logout(request)
        return redirect("/users/login/")
    return render(request, "auth/logout.html")


@login_required
def get_profile(request):
    user_service = ServiceContainer.user_service()

    try:
        user_dto = user_service.get_profile(request.user.id)
    except InstanceNotExistError:
        return render(request, "not_found.html", {"message": "Профіль користувача не знайдено!"})

    return render(request, "auth/profile.html", {"user_dto": user_dto})
