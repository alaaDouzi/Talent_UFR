from django.urls import path
from etudiant import views

urlpatterns = [
    path('stage', views.create_stage),
    path('stage/<int:id>', views.update_stage),
    path('myStages', views.my_stages),
    path('organismeAccueil', views.organisme_accueil),
]
