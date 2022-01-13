from django.urls import path
from etudiant import views

urlpatterns = [
    path('stage', views.create_stage),
    path('myStages', views.my_stages),
    path('organisme_accueil', views.organisme_accueil),
]
