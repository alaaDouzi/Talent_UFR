from django.db import models
from django.contrib.auth.models import User


class Filiere(models.Model):
    identifiant = models.CharField(
        primary_key=True, unique=True, max_length=20)
    designation = models.TextField()


class Mot_cle(models.Model):
    designation = models.TextField()
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)


class Tuteur(models.Model):
    nom = models.TextField()
    prenom = models.TextField()
    email = models.EmailField()
    telephone = models.TextField()


class Etudiant(models.Model):
    identifiant = models.CharField(
        primary_key=True, unique=True, max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    almuni_email = models.EmailField()
    alumni = models.BooleanField(default=False)
    telephone = models.CharField(max_length=15)
    filiere = models.ForeignKey(Filiere, on_delete=models.PROTECT)
    adresse = models.TextField()
    securite_sociale = models.TextField()
    num_securite_sociale = models.TextField()
    compagnie_responsabilite_civile = models.TextField()
    num_responsabilite_civile = models.TextField()


"""
username
password
email
first_name
last_name
"""
