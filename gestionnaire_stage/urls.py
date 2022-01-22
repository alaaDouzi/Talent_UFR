from django.urls import path
from gestionnaire_stage import views

urlpatterns = [
    path('stages', views.stages),
]
