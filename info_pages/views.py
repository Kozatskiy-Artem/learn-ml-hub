from django.shortcuts import render


def home(request):
    """"""

    return render(request, 'info_pages/home.html')


def ml_page(request):
    """"""

    return render(request, 'info_pages/ml.html')


def ml_types_page(request):
    """"""

    return render(request, 'info_pages/ml_types.html')


def neural_networks_page(request):
    """"""

    return render(request, 'info_pages/neural_networks.html')


def deep_learning_page(request):
    """"""

    return render(request, 'info_pages/deep_learning.html')
