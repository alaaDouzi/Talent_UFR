# Generated by Django 3.2.9 on 2022-01-12 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entreprise', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisme_accueil',
            name='codePostal',
            field=models.CharField(max_length=10),
        ),
    ]
