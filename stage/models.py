from django.db import models
from sqlalchemy import false
from ufr_st.models import Etudiant, Mot_cle, Tuteur
from entreprise.models import Organisme_Accueil, Responsable_administratif, Lieu, Maitre_stage, Proposeur_stage
from django.utils import timezone


class Etat(models.TextChoices):
    SUJET_BROUILLON = 'brouillon de sujet',  # sujet non soumis
    SUJET_EN_ATTENTE_VALIDATION = 'sujet en Attente validation',  # sujet soumis
    SUJET_VALIDE = 'sujet validé',
    SUJET_SOUS_REVERVE = 'sujet sous reserve',
    SUJET_REJETE = 'sujet rejeté',
    SUJET_CONFIRME = 'sujet confirmé',
    SUJET_ABANDONNE = 'sujet abandonné',
    STAGE_VALIDE = 'stage validé',
    EN_COURS_DE_REALISATION_CONVENTION = 'En cours de réalisation de convetion',
    STAGE_PRET = 'stage prêt à débuter',
    STAGE_EN_COURS = 'stage en cours',
    STAGE_ANNULE_PAR_ENTREPRISE = "stage annulé par l'entreprise",
    STAGE_TERMINE = 'stage terminé',  # arrivé à date_fin
    STAGE_CLOTURE = 'stage cloturé',  # arrivé à date_fin + soutenance effectuée
    STAGE_ARCHIVE = 'stage archivé',


class Modalites_versements(models.TextChoices):
    VIREMENT = 'Virement',
    CHEQUE = 'Chèque',
    ESPECE = 'Espèce',
    NON_CONNU = 'Non connu',


class Session_soutenance(models.TextChoices):
    SEPTEMBRE = 'septembre'
    JUIN = 'juin'


class Stage(models.Model):
    etat = models.CharField(
        max_length=45, choices=Etat.choices, default=Etat.SUJET_EN_ATTENTE_VALIDATION)
    intitule = models.TextField()  # sujet stage
    description = models.TextField()
#    documents_sup = models.FileField(null=True)
    date_debut = models.DateField()
    date_fin = models.DateField()
    jours_travail = models.TextField()
    horraire_travail = models.TextField()
    date_debut_interruption = models.DateField(null=True)
    date_fin_interruption = models.DateField(null=True)
    nombre_heure = models.IntegerField()  # nombre_heure par semaine
    remunere = models.BooleanField()
    en_france = models.BooleanField(default=True)
    confidentiel = models.BooleanField(default=False)
    remuneration = models.IntegerField()
    modalites_versements = models.CharField(
        max_length=15, choices=Modalites_versements.choices, default=Modalites_versements.NON_CONNU)
    avantage = models.TextField(blank=True)
    # lu et accepte text lois
    date_creation = models.DateTimeField(default=timezone.now)

    date_validation = models.DateTimeField(null=True)
    remarque_reserve = models.TextField(null=True, blank=False)
    raison_refus = models.TextField(null=True, blank=False)

    date_confirmarion = models.DateTimeField(null=True)

    date_attribution_tuteur = models.DateTimeField(null=True)

    date_prise_en_charge_convention = models.DateTimeField(null=True)

    # might be better to change it to an URL to drive or something like that
    convention = models.FileField(null=True, upload_to='uploads/')
    data_ajout_convention = models.DateTimeField(null=True)

    date_annulation_entreprise = models.DateTimeField(null=True)
    raison_annulation_entreprise = models.TextField(null=True)

    date_soutenance = models.DateTimeField(null=True)
    soutenance_effectuee = models.BooleanField(default=False)

    date_archive = models.DateTimeField(null=True)

    entreprise = models.ForeignKey(
        Organisme_Accueil, on_delete=models.RESTRICT)
    representant_etablissement = models.ForeignKey(
        Responsable_administratif, on_delete=models.RESTRICT)
    maitre_stage = models.ForeignKey(Maitre_stage, on_delete=models.RESTRICT)
    lieu = models.ForeignKey(Lieu, on_delete=models.RESTRICT)
    ayant_propose_stage = models.ForeignKey(
        Proposeur_stage, on_delete=models.RESTRICT)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.RESTRICT)
    tuteur = models.ForeignKey(Tuteur, on_delete=models.RESTRICT, null=True)
    list_mot_cle = models.ManyToManyField(Mot_cle)


class Retour_exprience(models.Model):
    mention = models.TextField()  # choice
    remarque = models.TextField()
    embauche = models.BooleanField()
    evaluation_entrerise = models.FloatField()  # evaluation /5 ou /10
    stage = models.OneToOneField(Stage, on_delete=models.CASCADE)
