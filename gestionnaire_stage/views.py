from django.shortcuts import render
from rest_framework import status
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from etudiant.serializers import EtudiantSerializer
# import request
from stage.models import Stage, Etat
from ufr_st.models import Mot_cle, Etudiant, Tuteur
from entreprise.models import Organisme_Accueil
from .serializers import StageAttributionTuteurSerializer, StageSerializer, OrganismeAccueilSerializer, ProposeurStageSerializer, MaitreStageSerializer, MotCleSerializer, TuteurSerializer, StageValidateSerializer, StageRefusSerializer, StageSousReserveSerializer, EtudiantSerializer, StageScheduleDateDefenseSerializer


@api_view(['GET'])
def stages(request):
    if request.method == 'GET':
        etat_query = request.query_params.get('etat')
        etudiant_id_query = request.query_params.get('etudiantId')
        entreprise_nom_query = request.query_params.get(
            'organismeAccueilNom')
        mot_cle_query = request.query_params.get(
            'motCle')
        filiere_query = request.query_params.get(
            'filiere')
        filters = {}

        if etat_query:
            filters['etat'] = etat_query
        if etudiant_id_query:
            filters['etudiant__identifiant'] = etudiant_id_query
        if entreprise_nom_query:
            filters['entreprise__nom'] = entreprise_nom_query
        if mot_cle_query:
            filters['list_mot_cle__designation'] = mot_cle_query
        if filiere_query:
            filters['etudiant__filiere__'] = filiere_query

        list_stage = Stage.objects.filter(**filters).all()

        response = []
        for stage in list_stage:
            list_mot_cle = []
            for mot_cle in stage.list_mot_cle.all():
                list_mot_cle.append(MotCleSerializer(mot_cle).data)
            element = {"stage": StageSerializer(
                stage).data,
                "entreprise": OrganismeAccueilSerializer(stage.entreprise).data,
                "maitre_stage": MaitreStageSerializer(stage.maitre_stage).data,
                "ayant_propose_stage": ProposeurStageSerializer(stage.ayant_propose_stage).data,
                "list_mot_cle": list_mot_cle,
            }
            if stage.tuteur != None:
                element["tuteur"] = TuteurSerializer(stage.tuteur).data
            response.append(element)
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def validate_sujet(request, id):
    if request.method == 'PUT':

        try:
            stage = Stage.objects.get(id=id)
        except Stage.DoesNotExist:
            error_message = f"Stage with id : {id} doesn\'t exist"
            return Response({"message": error_message}, status=status.HTTP_404_NOT_FOUND)

        stage_serializer = StageValidateSerializer(
            stage, data={"etat": Etat.SUJET_VALIDE, "date_validation": datetime.now()})

        if stage_serializer.is_valid():
            stage_serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(stage_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def refuser_sujet(request, id):
    if request.method == 'PUT':
        refus_data = request.data

        try:
            stage = Stage.objects.get(id=id)
        except Stage.DoesNotExist:
            error_message = f"Stage with id : {id} doesn\'t exist"
            return Response({"message": error_message}, status=status.HTTP_404_NOT_FOUND)

        refus_data["etat"] = Etat.SUJET_REJETE
        refus_data["date_validation"] = datetime.now()

        stage_serializer = StageRefusSerializer(
            stage, data=refus_data)

        if stage_serializer.is_valid():
            stage_serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(stage_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def sous_reserve_sujet(request, id):
    if request.method == 'PUT':
        sous_reserve_data = request.data

        try:
            stage = Stage.objects.get(id=id)
        except Stage.DoesNotExist:
            error_message = f"Stage with id : {id} doesn\'t exist"
            return Response({"message": error_message}, status=status.HTTP_404_NOT_FOUND)

        sous_reserve_data["etat"] = Etat.SUJET_SOUS_REVERVE

        stage_serializer = StageSousReserveSerializer(
            stage, data=sous_reserve_data)

        if stage_serializer.is_valid():
            stage_serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(stage_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
# valider STAGER par la meme occasion
def attribuer_tuteur(request, id):
    if request.method == 'PUT':
        stage_data = request.data
        tuteur_id = request.data.get("tuteurId")

        try:
            stage = Stage.objects.get(id=id)
        except Stage.DoesNotExist:
            error_message = f"Stage with id : {id} doesn\'t exist"
            return Response({"message": error_message}, status=status.HTTP_404_NOT_FOUND)

        if tuteur_id == None:
            return Response({"message": "system can't find 'tuteurId' in the body of the request"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            Tuteur.objects.get(id=tuteur_id)
        except Tuteur.DoesNotExist:
            error_message = f"Tuteur with id : {tuteur_id} doesn\'t exist"
            return Response({"message": error_message}, status=status.HTTP_404_NOT_FOUND)

        stage_data["etat"] = Etat.STAGE_VALIDE
        stage_data["tuteur"] = tuteur_id

        stage_serializer = StageAttributionTuteurSerializer(
            stage, data=stage_data)

        if stage_serializer.is_valid():
            stage_serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(stage_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_etudiants(request):
    if request.method == 'GET':
        etudiant_id_query = request.query_params.get('etudiantId')
        alumni_query = request.query_params.get(
            'alumni')
        filiere_query = request.query_params.get(
            'filiere')
        filters = {}

        if etudiant_id_query:
            filters['identifiant__startswith'] = etudiant_id_query
        if alumni_query:
            filters['alumni'] = alumni_query
        if filiere_query:
            filters['filiere'] = filiere_query

        list_etudiant = Etudiant.objects.filter(**filters).all()
        serializer = EtudiantSerializer(list_etudiant, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def programmer_date_soutenance(request, id):
    # STAGE_EN_COURS
    if request.method == 'PUT':
        date_soutenance = request.data.get("date_soutenance")

        try:
            stage = Stage.objects.get(id=id)
        except Stage.DoesNotExist:
            error_message = f"Stage with id : {id} doesn\'t exist"
            return Response({"message": error_message}, status=status.HTTP_404_NOT_FOUND)

        stage_serializer = StageScheduleDateDefenseSerializer(
            stage, data={"date_soutenance": date_soutenance})

        if stage_serializer.is_valid():
            stage_serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(stage_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
