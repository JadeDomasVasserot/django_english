from random import choice
from datetime import datetime, timedelta

from django.shortcuts import render, redirect

from .form import InscriptionForm, ConnexionForm, GameForm
from .models import Joueur, Ville, Verbe, Partie, Question


# Create your views here.
def accueil(request):
    if request.method == 'POST':
        form = ConnexionForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            motDePasse = form.cleaned_data['motDePasse']
            user = Joueur.objects.filter(motDePasse=motDePasse, email=email)
            
            partie = Partie(idJoueur = 1)
            partie.save()

            if user is not None:
                return redirect('jeu/'+ str(partie.id))

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
            joueur.save()
            return redirect('accueil')
    else:
        form = InscriptionForm()
    return render(request, 'inscription.html', {'form': form})


def jeu(request, idPartie):
    
    # Set up the initial score and timer values
    score = 0
    
    verb = choice(list(Verbe.objects.all()))# Génère un verbe aléatoire
    
    # Initialise les valeur de question 
    question = Question(
        idPartie = idPartie, 
        idVerbe = verb.id, 
        reponsePreterit = '', 
        reponseParticipePasse = '', 
        dateEnvoi = datetime.now(), 
        dateReponse = ''
    )  
    Question.save(question)
    
    form = GameForm()  
        
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            preterit = form.cleaned_data['preterit']
            participePasse = form.cleaned_data['participePasse']
            
            # Recupère l'instance de question 
            # question = Question.objects.get(pk=request.POST['question_id'])
            
            # Calcule le temps de différencce 
            time_diff = datetime.now() - question.dateEnvoi
            
            # Vérification des conditions 
            if preterit == verb.preterit and participePasse == verb.participePasse and time_diff <= timedelta(seconds=60):
                score += 1
                
                # Modification de question
                question.reponsePreterit = preterit
                question.reponseParticipePasse = participePasse
                question.dateReponse = datetime.now()
                question.save()
                
                # Choisis un nouveaux nombre aléatoire 
                verb = choice(list(Verbe.objects.all()))
            else:
                # Redirect vers la page de fin 
                return redirect('fin')
    
    return render(request, 'jeu.html', {'form': form, 'verb': verb, 'counter': score + 1, 'question_id': question.id})


def fin(request):
    return render(request, 'fin.html')
