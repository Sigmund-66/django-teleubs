from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("telateste", views.telateste, name="telateste")
]