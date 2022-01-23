from django.urls import path
from gestionnaire_stage import views

urlpatterns = [
    path('stages', views.stages),
    path('stage/<int:id>/validate', views.validate_stage),
    path('stage/<int:id>/refuser', views.refuser_stage),
    path('stage/<int:id>/sousReserve', views.sous_reserve_stage),
    path('stage/<int:id>/attribuerTuteur', views.attribuer_tuteur),
    path('etudiants', views.get_etudiants),

]
