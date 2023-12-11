from django.contrib import admin

from .models import ClassificationModel, HistoryModel, ImageModel

admin.site.register(ImageModel)
admin.site.register(ClassificationModel)
admin.site.register(HistoryModel)
