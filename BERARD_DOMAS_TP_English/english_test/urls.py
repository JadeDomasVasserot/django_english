from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('index/', views.accueil, name="accueil"),
    path('inscription/', views.inscription, name="inscription"),
    path('jeu/<int:id>/', views.jeu, name="jeu"),
    path('fin/', views.fin, name="fin"),
]
