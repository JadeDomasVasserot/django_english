from django.contrib import admin
from django.urls import path, include

from english_test import views

urlpatterns = [
    path('index/', views.accueil, name="accueil"),
    path('inscription/', views.inscription, name="inscription"),
]
