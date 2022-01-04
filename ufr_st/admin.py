from django.contrib import admin

from .models import Filiere, Mot_cle, Etudiant, Tuteur
# Register your models here.
admin.site.register(Filiere)
admin.site.register(Mot_cle)
admin.site.register(Etudiant)
admin.site.register(Tuteur)
