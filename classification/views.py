from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.containers import ServiceContainer

from .dto import CreateImageDTO, HyperParamsDTO
from .forms import HyperParamsForm, ImageUploadForm


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


@login_required
def create_model(request):
    """
        View for handling the creation of a classification model based on user-provided hyperparameters.

        This view expects a POST request with form data containing hyperparameters. Upon successful form validation,
        it uses the Classification Service to create a model, retrieves the training history, and renders a page
        displaying model metrics over epochs.
    """

    if request.method == "POST":
        form = HyperParamsForm(request.POST)
        if form.is_valid():
            hyper_params_dto = HyperParamsDTO(**form.cleaned_data)
            classification_service = ServiceContainer.classification_service()
            model_dto = classification_service.create_model(request.user, hyper_params_dto)

            epochs, accuracy, val_accuracy, loss, val_loss = zip(
                *[
                    (epoch.epoch_number, epoch.accuracy, epoch.val_accuracy, epoch.loss, epoch.val_loss)
                    for epoch in model_dto.history
                ]
            )

            context = {
                "accuracy": accuracy,
                "val_accuracy": val_accuracy,
                "epochs": epochs,
                "loss": loss,
                "val_loss": val_loss,
                "model_dto": model_dto,
            }
            return render(request, "classification/user_model.html", context)

    form = HyperParamsForm()
    return render(request, "classification/create_model.html", {"form": form})
