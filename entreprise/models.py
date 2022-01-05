from django.db import models
from django.utils.translation import gettext_lazy as _


class Organisme_Accueil(models.Model):
    nom = models.TextField(unique=True)
    adresse = models.TextField()
    codePostal = models.CharField(max_length=5)
    ville = models.TextField()
    pays = models.TextField()
    num_siret = models.TextField()


class Lieu(models.Model):
    serviceAffectation = models.TextField()
    adresse = models.TextField()
    codePostal = models.CharField(max_length=5)
    ville = models.TextField()
    pays = models.TextField()
    telephone = models.CharField(max_length=15)
    email = models.EmailField()
    entreprise = models.ForeignKey(Organisme_Accueil, on_delete=models.CASCADE)


class Civilte(models.TextChoices):
    MONSIEUR = 'M', _('Monsieur')
    MADAME = 'Mme', _('Madame')
    MADEMOISELLE = 'Mlle', _('Mademoiselle')


class Responsable_administratif(models.Model):
    civilité = models.CharField(
        max_length=14, choices=Civilte.choices)
    nom = models.CharField(max_length=20)
    prenom = models.CharField(max_length=50)
    fonction = models.CharField(max_length=50)
    telephone = models.CharField(max_length=15)
    email = models.EmailField()
    nom_contact_administatif = models.CharField(max_length=20)
    prenom_contact_administatif = models.CharField(max_length=50)
    telephone_contact_administatif = models.CharField(max_length=15)
    email_contact_administatif = models.EmailField()
    entreprise = models.ForeignKey(Organisme_Accueil, on_delete=models.CASCADE)


class Maitre_stage(models.Model):
    civilité = models.CharField(
        max_length=14, choices=Civilte.choices)
    nom = models.CharField(max_length=20)
    prenom = models.CharField(max_length=50)
    fonction = models.CharField(max_length=50)
    adresse = models.TextField()
    codePostal = models.CharField(max_length=5)
    ville = models.TextField()
    pays = models.TextField()
    telephone = models.CharField(max_length=15)
    fax = models.CharField(max_length=15)
    email = models.EmailField()
    entreprise = models.ForeignKey(Organisme_Accueil, on_delete=models.CASCADE)


class Proposeur_stage(models.Model):
    civilité = models.CharField(
        max_length=14, choices=Civilte.choices)
    nom = models.CharField(max_length=20)
    prenom = models.CharField(max_length=50)
    telephone = models.CharField(max_length=15)
    email = models.EmailField()
    entreprise = models.ForeignKey(Organisme_Accueil, on_delete=models.CASCADE)
