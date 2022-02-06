from django.urls import path
from etudiant import views

urlpatterns = [
    path('stage', views.create_stage),
    path('stage/<int:id>', views.update_stage),
    path('stage/<int:id>/confirme', views.confirme_stage),
    path('myStages', views.my_stages),
    path('stage/<int:id>/getConvention', views.get_convention),
    path('organismeAccueil', views.organisme_accueil),
]
