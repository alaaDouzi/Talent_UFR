from django.shortcuts import render
from rest_framework import status
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
# import request
from stage.models import Stage, Etat
from ufr_st.models import Mot_cle, Etudiant
from entreprise.models import Organisme_Accueil
from .serializers import StageSerializer, OrganismeAccueilSerializer, ProposeurStageSerializer, MaitreStageSerializer, MotCleSerializer, TuteurSerializer, StageUpdateSerializer, StageRefusSerializer, StageSousReserveSerializer


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
            filters['etudiant__filiere'] = filiere_query

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
def validate_stage(request, id):
    if request.method == 'PUT':

        try:
            stage = Stage.objects.get(id=id)
        except Stage.DoesNotExist:
            error_message = f"Stage with id : {id} doesn\'t exist"
            return Response({"message": error_message}, status=status.HTTP_404_NOT_FOUND)

        stage_serializer = StageUpdateSerializer(
            stage, data={"etat": Etat.SUJET_VALIDE})

        if stage_serializer.is_valid():
            stage_serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(stage_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
