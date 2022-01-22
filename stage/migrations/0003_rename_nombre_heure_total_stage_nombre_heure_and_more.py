# Generated by Django 4.0.1 on 2022-01-14 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stage', '0002_auto_20220112_1610'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stage',
            old_name='nombre_heure_total',
            new_name='nombre_heure',
        ),
        migrations.AddField(
            model_name='stage',
            name='confidentiel',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='stage',
            name='date_fin',
            field=models.DateField(null=True),
        ),
    ]