from django.urls import path
from gestionnaire_stage import views

urlpatterns = [
    path('stages', views.stages),
    path('stage/<int:id>/validate', views.validate_sujet),
    path('stage/<int:id>/refuser', views.refuser_sujet),
    path('stage/<int:id>/sousReserve', views.sous_reserve_sujet),
    path('stage/<int:id>/attribuerTuteur', views.attribuer_tuteur),
    path('stage/<int:id>/programmerDateSoutenance',
         views.programmer_date_soutenance),

    path('etudiants', views.get_etudiants),

]
