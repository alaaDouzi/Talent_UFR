from django.urls import path
from scolarite import views

urlpatterns = [
    path('stages', views.stages),
    path('stage/<int:id>/debutEditionConvention',
         views.prise_en_charge_convention),
    path('stage/<int:id>/rejeter', views.rejeter),
    path('stage/<int:id>/ajouterConvention', views.ajouter_convention),
    path('stage/<int:id>/getConvention', views.get_convention),
    path('stage/<int:id>/annulationParEntreprise',
         views.annulation_par_entreprise),
    path('stage/<int:id>/cloturer', views.cloturer_stage),
]
