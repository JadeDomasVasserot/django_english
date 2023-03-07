from django.core import validators
from django.forms import forms


class InscriptionForm(forms.Form):
    email = forms.CharField(max_length=200, label="Email",
                            widget=forms.EmailInput(
                            ), validators=[validators.validate_email])
    nom = forms.CharField(max_length=100, label="Nom",
                          widget=forms.TextInput(
                          ))
    prenom = forms.CharField(max_length=100, label="prenom",
                             widget=forms.TextInput(
                             ))
    motDePasse = forms.CharField(max_length=20, label="Mot de passe",
                          widget=forms.PasswordInput(
                          ))
    niveau = forms.CharField(max_length=100, label="Niveau",
                               widget=forms.TextInput(
                               ))
    idVille_id = forms.CharField(max_length=100, label="Ville",
                             widget=forms.TextInput(
                             ))


class ConnexionForm(forms.Form):
    email = forms.CharField(max_length=200, label="Email",
                            widget=forms.EmailInput(
                            ), validators=[validators.validate_email])
    motDePasse = forms.CharField(max_length=20, label="Mot de passe",
                                 widget=forms.PasswordInput(
                                 ))