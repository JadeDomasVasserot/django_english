from django.core import validators
from django import forms

from .models import Ville


class InscriptionForm(forms.Form):
    email = forms.CharField(max_length=200, label="Email",
                            widget=forms.EmailInput(
                            ), validators=[validators.validate_email], required=True)
    nom = forms.CharField(max_length=100, label="Nom",
                          widget=forms.TextInput(
                          ))
    prenom = forms.CharField(max_length=100, label="Prenom",
                             widget=forms.TextInput(
                             ), required=True)
    motDePasse = forms.CharField(max_length=20, label="Mot de passe",
                                 widget=forms.PasswordInput(
                                 ), required=True)
    conf_mdp = forms.CharField(max_length=20, label="Confirmer Mot de passe",
                               widget=forms.PasswordInput(
                               ), required=True)
    idVille_id = forms.ModelChoiceField(label="Ville", empty_label="Sélectionner une ville",
                                        queryset=Ville.objects.all(), required=True)


class ConnexionForm(forms.Form):
    email = forms.CharField(max_length=200, label="Email",
                            widget=forms.EmailInput(
                            ), validators=[validators.validate_email])
    motDePasse = forms.CharField(max_length=20, label="Mot de passe",
                                 widget=forms.PasswordInput(
                                 ))


class GameForm(forms.Form):
    preterit = forms.CharField(max_length=200, label="Prétérit",
                               widget=forms.TextInput(
                               ))
    participePasse = forms.CharField(max_length=200, label="Participe Passé",
                                     widget=forms.TextInput(
                                     ))
