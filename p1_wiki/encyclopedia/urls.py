from re import search
from encyclopedia.views import random
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="new"),
    path("randomPage", views.randomPage, name="randomPage"),
    path("search", views.search, name="search"),
    # path("edit", views.edit, name="edit"),
    path("<str:title>", views.title, name="title")
]
