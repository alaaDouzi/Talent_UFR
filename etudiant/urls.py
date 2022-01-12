from django.urls import path
from etudiant import views

urlpatterns = [
    path('stage', views.stage),
    path('organisme_accueil', views.organisme_accueil),
]
