from django.urls import path

from . import views

app_name = "documents"

urlpatterns = [
    path('index', views.DocumentIndex.as_view(), name="index"),
    path('createDocument', views.DocumentCreate.as_view(), name="create"),
    path('editDocument/<int:pk>', views.DocumentEdit.as_view(), name="edit"),
    path('switchActiveDocument/<int:pk>', views.DocumentSwitchActive, name="switchActive"),
    path('deleteDocument/<int:pk>', views.DocumentDelete.as_view(), name="delete"),
]
