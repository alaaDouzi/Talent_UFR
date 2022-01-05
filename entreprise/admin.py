from django.contrib import admin
from .models import Organisme_Accueil, Lieu, Responsable_administratif, Maitre_stage, Proposeur_stage
# Register your models here.
admin.site.register(Organisme_Accueil)
admin.site.register(Lieu)
admin.site.register(Responsable_administratif)
admin.site.register(Maitre_stage)
admin.site.register(Proposeur_stage)
