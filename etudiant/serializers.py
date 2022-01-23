from rest_framework import serializers
from stage.models import Stage
from ufr_st.models import Etudiant, Mot_cle, Tuteur
from entreprise.models import Organisme_Accueil, Lieu, Responsable_administratif, Maitre_stage, Proposeur_stage


class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ['id', 'etat', 'intitule', 'description', 'date_debut', 'date_fin',
                  'date_debut_interruption', 'date_fin_interruption', 'nombre_heure',
                  'remunere', 'en_france', 'confidentiel', 'remuneration', 'modalites_versements', 'avantage', 'date_creation', 'date_validation', 'remarque_reserve',  'raison_refus', 'date_confirmarion', 'date_prise_en_charge_convention', 'date_annulation_entreprise', 'raison_annulation_entreprise', 'date_soutenance']


class StageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ['id', 'intitule', 'description', 'date_debut', 'date_fin',
                  'date_debut_interruption', 'date_fin_interruption', 'nombre_heure',   'remunere', 'en_france', 'confidentiel',
                  'remuneration', 'modalites_versements', 'avantage', 'entreprise',
                  'representant_etablissement', 'maitre_stage', 'lieu', 'ayant_propose_stage', 'etudiant']


class StageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ['intitule', 'description', 'date_debut', 'date_fin',
                  'date_debut_interruption', 'date_fin_interruption', 'nombre_heure',
                  'remunere', 'remuneration', 'en_france', 'confidentiel', 'modalites_versements', 'avantage']


class OrganismeAccueilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisme_Accueil
        fields = ['id', 'nom', 'adresse',
                  'codePostal', 'ville', 'pays', 'num_siret']


class LieuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lieu
        fields = ['id', 'serviceAffectation', 'adresse',
                  'codePostal', 'ville', 'pays', 'telephone', 'email', 'entreprise']


class ResponsableAdministratifSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsable_administratif
        fields = ['id', 'civilité', 'nom', 'prenom', 'fonction',
                  'telephone', 'email', 'nom_contact_administatif', 'prenom_contact_administatif',
                  'telephone_contact_administatif', 'email_contact_administatif', 'entreprise']


class MaitreStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maitre_stage
        fields = ['id', 'civilité', 'nom', 'prenom', 'fonction',
                  'adresse', 'codePostal', 'ville', 'pays',
                  'telephone', 'fax', 'email', 'entreprise']


class ProposeurStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposeur_stage
        fields = ['id', 'civilité', 'nom', 'prenom', 'telephone',
                  'email', 'entreprise']


class EtudiantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etudiant
        fields = ['identifiant', 'user', 'almuni_email', 'alumni', 'telephone',
                  'filiere', 'adresse', 'securite_sociale', 'num_securite_sociale',
                  'compagnie_responsabilite_civile', 'num_responsabilite_civile']


class TuteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tuteur
        fields = ['id', 'nom', 'prenom', 'email', 'telephone']


class MotCleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mot_cle
        fields = ['id', 'designation', 'filiere']
