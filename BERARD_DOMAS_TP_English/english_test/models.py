from django.db import models


# Create your models here.

class Ville(models.Model):
    cp = models.CharField(max_length=10)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Joueur(models.Model):
    email = models.CharField(max_length=200)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    motDePasse = models.CharField(max_length=20)
    idVille = models.ForeignKey('Ville', on_delete=models.PROTECT)
    niveau = models.IntegerField()

    def __str__(self):
        return self


class Partie(models.Model):
    idJoueur = models.ForeignKey('Joueur', on_delete=models.PROTECT)
    score = models.IntegerField()

    def __str__(self):
        return self


class Question(models.Model):
    idPartie = models.ForeignKey('Partie', on_delete=models.PROTECT)
    idVerbe = models.ForeignKey('Verbe', on_delete=models.PROTECT)
    reponsePreterit = models.CharField(max_length=100)
    reponseParticipePasse = models.CharField(max_length=100)
    dateEnvoi = models.DateTimeField(auto_now_add=True, auto_now=False,
                                     verbose_name="date d'envoi")
    dateReponse = models.DateTimeField(auto_now_add=True, auto_now=False,
                                       verbose_name="date de réponse")  # date et heure

    def __str__(self):
        return self


class Verbe(models.Model):
    baseVerbale = models.CharField(max_length=100)
    preterit = models.CharField(max_length=100)
    participePasse = models.CharField(max_length=100)
    traduction = models.CharField(max_length=100)

    def __str__(self):
        return self
