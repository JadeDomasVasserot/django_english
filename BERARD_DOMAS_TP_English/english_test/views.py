from random import choice

from django.shortcuts import render, redirect

from .form import InscriptionForm, ConnexionForm, GameForm
from .models import Joueur, Ville, Verbe


# Create your views here.
def accueil(request):
    if request.method == 'POST':
        form = ConnexionForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            motDePasse = form.cleaned_data['motDePasse']
            user = Joueur.objects.filter(motDePasse=motDePasse, email=email)

            if user is not None:
                return redirect('jeu')

    else:
        form = ConnexionForm()
    return render(request, 'index.html', {'form': form})


def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)

        if form.is_valid():
            nom = form.cleaned_data['nom']
            prenom = form.cleaned_data['prenom']
            email = form.cleaned_data['email']
            motDePasse = form.cleaned_data['motDePasse']
            city = form.cleaned_data['idVille_id'].id
            conf_mdp = form.cleaned_data['conf_mdp']
            joueur = Joueur(email=email, nom=nom, prenom=prenom, motDePasse=motDePasse, niveau=1, idVille_id=city)
            Joueur.save(joueur)
            return redirect('accueil')
    else:
        form = InscriptionForm()
    return render(request, 'inscription.html', {'form': form})


def jeu(request):
    # Set up the initial score and timer values
    score = 0
    remaining_time = 60
    # Generate a random verb from the list of irregular verbs
    verb = choice(list(Verbe.objects.all()))
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():

            print(1)
            preterit = form.cleaned_data['preterit']
            print(preterit)
            participePasse = form.cleaned_data['participePasse']
            print(participePasse)
            print(verb.preterit)
            if preterit == verb.preterit and participePasse == verb.participePasse:
                print(2)
                score += 1
            else:
                print(3)
                return redirect('fin')

    else:
        form = GameForm()
    return render(request, 'jeu.html', {'form': form, 'verb': verb, 'counter': score + 1})


def fin(request):
    return render(request, 'fin.html')
