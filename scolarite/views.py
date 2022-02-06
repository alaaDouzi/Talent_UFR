from django.http import FileResponse
from django.shortcuts import render
from rest_framework import status
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from etudiant.serializers import EtudiantSerializer
# import request
from stage.models import Stage, Etat
from .serializers import StageAnnulationEntrepriseSerializer, StageSerializer, OrganismeAccueilSerializer, MaitreStageSerializer, EtudiantSerializer, LieuSerializer, ResponsableAdministratifSerializer, StagePriseEnChargeConventionSerializer, StageAjouterConventionSerializer, StageCloturerSerializer, StageRejetSerializer

# Create your views here.


@api_view(['GET'])
def stages(request):
    if request.method == 'GET':
        etat_query = request.query_params.get('etat')
        entreprise_nom_query = request.query_params.get(
            'organismeAccueilNom')
        filiere_query = request.query_params.get(
            'filiere')
        filters = {}

        if etat_query:
            filters['etat'] = etat_query
        if entreprise_nom_query:
            filters['entreprise__nom'] = entreprise_nom_query
        if filiere_query:
            filters['etudiant__filiere'] = filiere_query

        list_etat = [Etat.STAGE_VALIDE, Etat.EN_COURS_DE_REALISATION_CONVENTION,
                     Etat.STAGE_PRET, Etat.STAGE_EN_COURS]

        list_stage = Stage.objects.filter(
            **filters).filter(etat__in=list_etat).all()

        response = []
        for stage in list_stage:
            element = {"stage": StageSerializer(
                stage).data,
                "entreprise": OrganismeAccueilSerializer(stage.entreprise).data,
                "lieu": LieuSerializer(stage.lieu).data,
                "representant_etablissement": ResponsableAdministratifSerializer(stage.representant_etablissement).data,
                "maitre_stage": MaitreStageSerializer(stage.maitre_stage).data,
                "etudiant": EtudiantSerializer(stage.etudiant).data
            }
            response.append(element)
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def prise_en_charge_convention(request, id):
    if request.method == 'PUT':
        try:
            stage = Stage.objects.get(id=id)
        except Stage.DoesNotExist:
            error_message = f"Stage with id : {id} doesn\'t exist"
            return Response({"message": error_message}, status=status.HTTP_404_NOT_FOUND)

        stage_serializer = StagePriseEnChargeConventionSerializer(
            stage, data={"etat": Etat.EN_COURS_DE_REALISATION_CONVENTION, "date_prise_en_charge_convention": datetime.now()})

        if stage_serializer.is_valid():
            stage_serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(stage_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def rejeter(request, id):
    if request.method == 'PUT':
        rejet_data = request.data

        try:
            stage = Stage.objects.get(id=id)
        except Stage.DoesNotExist:
            error_message = f"Stage with id : {id} doesn\'t exist"
            return Response({"message": error_message}, status=status.HTTP_404_NOT_FOUND)

        rejet_data["etat"] = Etat.SUJET_REJETE

        stage_serializer = StageRejetSerializer(
            stage, data=rejet_data)

        if stage_serializer.is_valid():
            stage_serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(stage_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def ajouter_convention(request, id):
    if request.method == 'PUT':
        aout_convention_data = request.data
        try:
            stage = Stage.objects.get(id=id)
        except Stage.DoesNotExist:
            error_message = f"Stage with id : {id} doesn\'t exist"
            return Response({"message": error_message}, status=status.HTTP_404_NOT_FOUND)

        aout_convention_data["etat"] = Etat.STAGE_PRET
        aout_convention_data["data_ajout_convention"] = datetime.now()

        stage_serializer = StageAjouterConventionSerializer(
            stage, data=aout_convention_data)
        if stage_serializer.is_valid():
            stage_serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(stage_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_convention(request, id):
    if request.method == 'GET':

        try:
            stage = Stage.objects.get(id=id)
        except Stage.DoesNotExist:
            error_message = f"Stage with id : {id} doesn\'t exist"
            return Response({"message": error_message}, status=status.HTTP_404_NOT_FOUND)

        convention = stage.convention.open()
        response = FileResponse(convention)
        return response
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def annulation_par_entreprise(request, id):
    if request.method == 'PUT':
        annulation_data = request.data

        try:
            stage = Stage.objects.get(id=id)
        except Stage.DoesNotExist:
            error_message = f"Stage with id : {id} doesn\'t exist"
            return Response({"message": error_message}, status=status.HTTP_404_NOT_FOUND)

        annulation_data["etat"] = Etat.STAGE_ANNULE_PAR_ENTREPRISE
        annulation_data["date_annulation_entreprise"] = datetime.now()

        stage_serializer = StageAnnulationEntrepriseSerializer(
            stage, data=annulation_data)

        if stage_serializer.is_valid():
            stage_serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(stage_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def cloturer_stage(request, id):
    if request.method == 'PUT':
        try:
            stage = Stage.objects.get(id=id)
        except Stage.DoesNotExist:
            error_message = f"Stage with id : {id} doesn\'t exist"
            return Response({"message": error_message}, status=status.HTTP_404_NOT_FOUND)

        data = {"soutenance_effectuee": True}
        if stage.etat == Etat.STAGE_TERMINE:
            data["etat"] = Etat.STAGE_CLOTURE

        stage_serializer = StageCloturerSerializer(
            stage, data=data)

        if stage_serializer.is_valid():
            stage_serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(stage_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
