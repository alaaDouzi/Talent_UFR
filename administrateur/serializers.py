from rest_framework import serializers
from ufr_st.models import Filiere, Mot_cle, Tuteur
from entreprise.models import Organisme_Accueil, Lieu, Responsable_administratif, Maitre_stage, Proposeur_stage
# Create your models here.


class MotCleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mot_cle
        fields = ['id', 'designation', 'filiere', 'actif']


class MotCleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mot_cle
        fields = ['designation', 'actif']


class FiliereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filiere
        fields = ['identifiant', 'designation']


class FiliereUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filiere
        fields = ['designation']


class TuteurSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tuteur
        fields = ['id', 'nom', 'prenom', 'email', 'telephone']
