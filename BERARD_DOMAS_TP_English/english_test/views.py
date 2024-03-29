from random import choice
from datetime import datetime, timedelta
from django.http import HttpResponseNotFound

import pytz

from django.utils import timezone

from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from .form import InscriptionForm, ConnexionForm, GameForm
from .models import Joueur, Ville, Verbe, Partie, Question

local_tz = pytz.timezone('Europe/Paris')


# Create your views here.
def accueil(request):
    bestUser = Joueur.objects.all().order_by('-niveau')[:5]
    if request.method == 'POST':
        form = ConnexionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            motDePasse = form.cleaned_data['motDePasse']
            user = Joueur.objects.filter(email=email, motDePasse=motDePasse).first()
            if user is not None:
                partie = Partie(idJoueur_id=user.id, score=0)
                partie.save()
                last_game = Partie.objects.filter(idJoueur=user.id).order_by('-id').first()
                if last_game:
                    # Do something with the last game object, e.g. redirect to the game view
                    return redirect('/jeu/{}'.format(partie.id))
                else:
                    # The user has not played any games yet, do something else
                    return redirect('index')
            else:
                form.add_error(None, "L'adresse email ou le mot de passe est incorrect.")

    else:
        form = ConnexionForm()
    return render(request, 'index.html', {'form': form, 'bestUser': bestUser})


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

            if motDePasse == conf_mdp:
                joueur = Joueur(email=email, nom=nom, prenom=prenom, motDePasse=motDePasse, niveau=1, idVille_id=city)
                Joueur.save(joueur)
                return redirect('accueil')
            else:
                form.add_error(None, "Les 2 mots de passe ne correspondent pas")
    else:
        form = InscriptionForm()
    return render(request, 'inscription.html', {'form': form})


def jeu(request, idPartie):
    try:
        partie = Partie.objects.get(pk=idPartie)
        user = Joueur.objects.get(pk=partie.idJoueur_id)
    except Partie.DoesNotExist:
        return HttpResponseNotFound("Partie non trouvée")

    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            preterit = form.cleaned_data['preterit']
            participePasse = form.cleaned_data['participePasse']

            # Recupère l'instance de question 
            question = Question.objects.filter(idPartie=partie.id).order_by('-dateEnvoi').first()

            # Calcule le temps de différencce 
            time_diff = datetime.now(tz=local_tz).astimezone(pytz.utc) - question.dateEnvoi
            time_diff = int(time_diff.total_seconds())

            # Vérification des conditions - and time_diff <= timedelta(seconds=60)
            if preterit == question.idVerbe.preterit and participePasse == question.idVerbe.participePasse and time_diff <= 60:
                # Modification de question
                question.reponsePreterit = preterit
                question.reponseParticipePasse = participePasse
                question.dateReponse = datetime.now()
                question.save()

                partie.score += 1
                partie.save()
            else:
                if partie.idJoueur.niveau == partie.score :
                    partie.idJoueur.niveau = partie.score
                
                # Redirect vers la page de fin 
                return redirect('/fin/{}'.format(partie.id))

    verb = choice(list(Verbe.objects.all()))  # Génère un verbe aléatoire

    # Initialise les valeur de question
    question = Question(
        idPartie=partie,
        idVerbe=verb,
        reponsePreterit='',
        reponseParticipePasse='',
        dateEnvoi=datetime.now(tz=local_tz).astimezone(pytz.utc),
        dateReponse=''
    )
    Question.save(question)

    form = GameForm()
    return render(request, 'jeu.html', {'form': form, 'verb': verb, 'counter': partie.score+1, 'question_id': question.id,
                                        'partie_id': partie.id, 'user': user})


def fin(request, idPartie):
    try:
        partie = Partie.objects.get(pk=idPartie)
        print(partie.id)
    except Partie.DoesNotExist:
        return HttpResponseNotFound("Partie non trouvée")

    question = Question.objects.filter(idPartie=partie.id).order_by('-dateEnvoi').first()

    partie2 = Partie(idJoueur_id=partie.idJoueur.id, score=0)
    partie2.save()
    
    print ('Partie = ', partie2.id)

    return render(request, 'fin.html',
                  {'joueur': partie.idJoueur, 'verbe': question.idVerbe, 'partie2Id': partie2.id, 'counter': partie.score, 'numero': partie.score + 1 })
