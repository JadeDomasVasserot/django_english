from django.contrib import admin

from .models import Joueur, Partie, Question, Verbe, Ville

# Register your models here.

admin.site.register(Joueur)
admin.site.register(Partie)
admin.site.register(Question)
admin.site.register(Verbe)
admin.site.register(Ville)
