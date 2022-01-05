from django.db import models
from ufr_st.models import Etudiant, Mot_cle, Tuteur
from entreprise.models import Organisme_Accueil, Responsable_administratif, Lieu, Maitre_stage, Proposeur_stage
from django.utils import timezone


class Etat(models.TextChoices):
    SUJET_EN_ATTENTE_VALIDATION = 'sujet en Attente validation',
    SUJET_VALIDE = 'sujet validé',
    SUJET_SOUS_REVERVE = 'sujet sous reserve',
    SUJET_REJETE = 'sujet rejeté',
    SUJET_CONFIRME = 'sujet confirmé',
    SUJET_ABANDONNE = 'sujet abandonné',
    STAGE_VALIDE = 'stage validé',
    EN_COURS_DE_REALISATION_CONVENTION = 'En cours de réalisation de convetion',
    STAGE_EN_COURS = 'stage en cours',
    STAGE_ANNULE_PAR_ENTREPRISE = "stage annulé par l'entreprise",
    STAGE_TERMINE = 'stage terminé',
    STAGE_ARCHIVE = 'stage archivé',


class Modalites_versements(models.TextChoices):
    VIREMENT = 'Virement',
    CHEQUE = 'Chèque',
    ESPECE = 'Espèce',
    NON_CONNU = 'Non connu',


class Stage(models.Model):
    etat = models.CharField(
        max_length=45, choices=Etat.choices, default=Etat.SUJET_EN_ATTENTE_VALIDATION)
    intitule = models.TextField()  # sujet stage
    description = models.TextField()
    documents_sup = models.FileField()
    date_debut = models.DateField()
    date_fin = models.DateField()
    # Jours et horaires de travail
    date_debut_interruption = models.DateField()
    date_fin_interruption = models.DateField()
    nombre_heure_total = models.IntegerField()
    remunere = models.BooleanField()
    remuneration = models.IntegerField()
    modalites_versements = models.CharField(
        max_length=15, choices=Modalites_versements.choices, default=Modalites_versements.VIREMENT)
    avantage = models.TextField()

    date_creation = models.DateTimeField(default=timezone.now)

    date_validation = models.DateTimeField()
    remarque_reserve = models.TextField()
    raison_refus = models.TextField()

    date_confirmarion = models.DateTimeField()

    date_prise_en_charge_convention = models.DateTimeField()

    date_annulation_entreprise = models.DateTimeField()
    raison_annulation_entreprise = models.DateTimeField()

    date_soutenance = models.DateTimeField()
    # session soutenance

    date_archive = models.DateTimeField()

    entreprise = models.ForeignKey(
        Organisme_Accueil, on_delete=models.RESTRICT)
    representant_etablissement = models.ForeignKey(
        Responsable_administratif, on_delete=models.RESTRICT)
    maitre_stage = models.ForeignKey(Maitre_stage, on_delete=models.RESTRICT)
    lieu = models.ForeignKey(Lieu, on_delete=models.RESTRICT)
    ayant_propose_stage = models.ForeignKey(
        Proposeur_stage, on_delete=models.RESTRICT)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.RESTRICT)
    tuteur = models.ForeignKey(Tuteur, on_delete=models.RESTRICT)
    list_mot_cle = models.ManyToManyField(Mot_cle)


class Retour_exprience(models.Model):
    mention = models.TextField()  # choice
    remarque = models.TextField()
    embauche = models.BooleanField()
    evaluation_entrerise = models.FloatField()  # evaluation /5 ou /10
    stage = models.OneToOneField(Stage, on_delete=models.CASCADE)
