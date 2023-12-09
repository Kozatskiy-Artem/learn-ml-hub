from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.containers import ServiceContainer

from .dto import CreateImageDTO
from .forms import ImageUploadForm


@login_required()
def cats_or_dogs(request):
    """
    Handle the Cats or Dogs classification view.

    If the request method is POST, process the uploaded image using the classification service.
    Display the uploaded image and the classification result.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse - The rendered HTML page.
    """

    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_dto = CreateImageDTO(user_id=request.user.id, **form.cleaned_data)

            classification_service = ServiceContainer.classification_service()
            image, prediction = classification_service.get_prediction(image_dto, "cats_or_dogs_model")

            form = ImageUploadForm()

            return render(
                request,
                "classification/cats_or_dogs.html",
                {"image": image, "prediction": prediction, "form": form},
            )

    form = ImageUploadForm()
    return render(request, "classification/cats_or_dogs.html", {"form": form})


@login_required()
def cats_or_dogs_pre_trained_model(request):
    """
    Handle the Cats or Dogs classification view.

    If the request method is POST, process the uploaded image using the classification service.
    Display the uploaded image and the classification result.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse - The rendered HTML page.
    """

    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_dto = CreateImageDTO(user_id=request.user.id, **form.cleaned_data)

            classification_service = ServiceContainer.classification_service()
            image, prediction = classification_service.get_prediction(image_dto, "cats_or_dogs_transfer_learned_model")

            form = ImageUploadForm()

            return render(
                request,
                "classification/cats_or_dogs_transfer_learned_model.html",
                {"image": image, "prediction": prediction, "form": form},
            )

    form = ImageUploadForm()
    return render(request, "classification/cats_or_dogs_transfer_learned_model.html", {"form": form})
