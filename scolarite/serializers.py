from rest_framework import serializers
from stage.models import Stage
from ufr_st.models import Etudiant, Mot_cle, Tuteur
from entreprise.models import Organisme_Accueil, Lieu, Responsable_administratif, Maitre_stage, Proposeur_stage


class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ['id', 'etat', 'intitule', 'description', 'date_debut', 'date_fin', 'jours_travail', 'horraire_travail',
                  'date_debut_interruption', 'date_fin_interruption', 'nombre_heure',
                  'remunere', 'en_france', 'confidentiel', 'remuneration', 'modalites_versements', 'avantage', 'date_prise_en_charge_convention', 'data_ajout_convention', 'date_soutenance', 'soutenance_effectuee', 'convention']


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


class EtudiantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Etudiant
        fields = ['identifiant', 'user', 'telephone', 'filiere', 'adresse', 'securite_sociale', 'num_securite_sociale',
                  'compagnie_responsabilite_civile', 'num_responsabilite_civile']
        depth = 2


class StagePriseEnChargeConventionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ['etat', 'date_prise_en_charge_convention']


class StageRejetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ['etat', 'raison_refus']


class StageAjouterConventionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ['etat', 'convention', 'data_ajout_convention']
        required_fields = ['etat', 'convention', 'data_ajout_convention']


class StageAnnulationEntrepriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ['etat', 'raison_annulation_entreprise',
                  'date_annulation_entreprise']


class StageCloturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ['etat', 'soutenance_effectuee']
        required_fields = ['soutenance_effectuee']
