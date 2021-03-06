# Generated by Django 3.2.9 on 2022-01-05 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organisme_Accueil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.TextField(unique=True)),
                ('adresse', models.TextField()),
                ('codePostal', models.CharField(max_length=5)),
                ('ville', models.TextField()),
                ('pays', models.TextField()),
                ('num_siret', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Responsable_administratif',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('civilité', models.CharField(choices=[('M', 'Monsieur'), ('Mme', 'Madame'), ('Mlle', 'Mademoiselle')], max_length=14)),
                ('nom', models.CharField(max_length=20)),
                ('prenom', models.CharField(max_length=50)),
                ('fonction', models.CharField(max_length=50)),
                ('telephone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('nom_contact_administatif', models.CharField(max_length=20)),
                ('prenom_contact_administatif', models.CharField(max_length=50)),
                ('telephone_contact_administatif', models.CharField(max_length=15)),
                ('email_contact_administatif', models.EmailField(max_length=254)),
                ('entreprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entreprise.organisme_accueil')),
            ],
        ),
        migrations.CreateModel(
            name='Proposeur_stage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('civilité', models.CharField(choices=[('M', 'Monsieur'), ('Mme', 'Madame'), ('Mlle', 'Mademoiselle')], max_length=14)),
                ('nom', models.CharField(max_length=20)),
                ('prenom', models.CharField(max_length=50)),
                ('telephone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('entreprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entreprise.organisme_accueil')),
            ],
        ),
        migrations.CreateModel(
            name='Maitre_stage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('civilité', models.CharField(choices=[('M', 'Monsieur'), ('Mme', 'Madame'), ('Mlle', 'Mademoiselle')], max_length=14)),
                ('nom', models.CharField(max_length=20)),
                ('prenom', models.CharField(max_length=50)),
                ('fonction', models.CharField(max_length=50)),
                ('adresse', models.TextField()),
                ('codePostal', models.CharField(max_length=5)),
                ('ville', models.TextField()),
                ('pays', models.TextField()),
                ('telephone', models.CharField(max_length=15)),
                ('fax', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('entreprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entreprise.organisme_accueil')),
            ],
        ),
        migrations.CreateModel(
            name='Lieu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serviceAffectation', models.TextField()),
                ('adresse', models.TextField()),
                ('codePostal', models.CharField(max_length=5)),
                ('ville', models.TextField()),
                ('pays', models.TextField()),
                ('telephone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('entreprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entreprise.organisme_accueil')),
            ],
        ),
    ]
