from random import choice
from datetime import datetime, timedelta
from django.http import HttpResponseNotFound

from django.utils import timezone

from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from .form import InscriptionForm, ConnexionForm, GameForm
from .models import Joueur, Ville, Verbe, Partie, Question


# Create your views here.
def accueil(request):
    bestUser = Joueur.objects.order_by('-niveau').first()
    if request.method == 'POST':
        form = ConnexionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            motDePasse = form.cleaned_data['motDePasse']
            user = Joueur.objects.filter(email=email, motDePasse=motDePasse).first()
            if user is not None:
                partie = Partie(idJoueur_id=user.id)
                Partie.save(partie)
                return redirect('/jeu/{}'.format(partie.id))
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
    # Set up the initial score and timer values
    score = 0
    
    try:
        partie = Partie.objects.get(pk=idPartie)
        print(partie.id)
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
            # time_diff = timezone.now() - timezone.make_aware(question.dateEnvoi, timezone.get_current_timezone())
            print (preterit),
            print (question.idVerbe.preterit)
            
            # Vérification des conditions - and time_diff <= timedelta(seconds=60)
            if preterit == question.idVerbe.preterit and participePasse == question.idVerbe.participePasse :
                score += 1
                # Modification de question
                question.reponsePreterit = preterit
                question.reponseParticipePasse = participePasse
                question.dateReponse = datetime.now()
                question.save()
            else:
                # Redirect vers la page de fin 
                return redirect('/fin/{}'.format(partie.id))
    
    verb = choice(list(Verbe.objects.all()))# Génère un verbe aléatoire
    
        # Initialise les valeur de question 
    question = Question(
        idPartie = partie,   
        idVerbe = verb, 
        reponsePreterit = '', 
        reponseParticipePasse = '', 
        dateEnvoi = datetime.now(), 
        dateReponse = ''
    )  
    Question.save(question)
    
    form = GameForm() 
    
    return render(request, 'jeu.html', {'form': form, 'verb': verb, 'counter': score + 1, 'question_id': question.id, 'partie_id': partie.id})


def fin(request, idPartie):
    try:
        partie = Partie.objects.get(pk=idPartie)
        print(partie.id)
    except Partie.DoesNotExist:
        return HttpResponseNotFound("Partie non trouvée") 
    
    question = Question.objects.filter(idPartie=partie.id).order_by('-dateEnvoi').first()
    
    return render(request, 'fin.html', {'joueur': partie.idJoueur, 'verbe': question.idVerbe})
