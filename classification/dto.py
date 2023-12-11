from typing import Optional

from django.core.files.uploadedfile import UploadedFile
from pydantic import BaseModel


class CreateImageDTO(BaseModel):
    user_id: int
    title: str
    image: Optional[UploadedFile | str] = None

    class Config:
        arbitrary_types_allowed = True


class ImageDTO(BaseModel):
    id: int
    user_id: int
    title: str
    image: str


class HyperParamsDTO(BaseModel):
    filters_1_layer: int
    filters_2_layer: int
    filters_3_layer: int
    dense_neurons: int
    epochs: int


class ModelDTO(BaseModel):
    id: int
    user_id: int
    filters_1_layer: int
    filters_2_layer: int
    filters_3_layer: int
    dense_neurons: int
    epochs: int
    weights_path: str
    history: list


class HistoryDTO(BaseModel):
    id: int
    class_model_id: int
    epoch_number: int
    accuracy: float
    val_accuracy: float
    loss: float
    val_loss: float
