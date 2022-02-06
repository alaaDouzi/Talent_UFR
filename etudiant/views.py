from datetime import datetime
from django.http import FileResponse
from rest_framework import status
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
# import request
from stage.models import Stage, Etat
from ufr_st.models import Mot_cle, Etudiant
from entreprise.models import Organisme_Accueil
from .serializers import StageConfirmationSerializer, StageSerializer, OrganismeAccueilSerializer, LieuSerializer, ResponsableAdministratifSerializer, ProposeurStageSerializer, MaitreStageSerializer, StageCreateSerializer, MotCleSerializer, TuteurSerializer, StageUpdateSerializer
from django.db.models import Q

# Create your views here.


@api_view(['POST'])
@transaction.atomic
def create_stage(request):
    if request.method == 'POST':
        stage_data = request.data.get("stage")
        # njibouh from cookies later
        etudiant_id = request.data.get("etudiantId")
        organisme_accueil_id = request.data.get("organismeAccueilId")
        lieu_data = request.data.get("lieu")
        responsable_administratif_data = request.data.get(
            "responsableAdministratif")
        maitre_stage_data = request.data.get("maitreStage")
        proposeur_stage_data = request.data.get("proposeurStage")
        list_mot_cle_data = request.data.get("list_mot_cle")

        # region organisme_accueil verification
        if organisme_accueil_id == None:
            return Response({"message": "system can't find 'organismeAccueilId' in the body of the request"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            Organisme_Accueil.objects.get(id=organisme_accueil_id)
        except Organisme_Accueil.DoesNotExist:
            error_message = f"Organisme_Accueil with id : {organisme_accueil_id} doesn\'t exist"
            return Response({"message": error_message}, status=status.HTTP_404_NOT_FOUND)
        # endregion

        # region etudiant verification
        if etudiant_id == None:
            return Response({"message": "system can't find 'etudiantId' in the body of the request"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            Etudiant.objects.get(identifiant=etudiant_id)
        except Etudiant.DoesNotExist:
            error_message = f"Etudiant with identifiant : {etudiant_id} doesn't exist"
            return Response({"message": error_message}, status=status.HTTP_404_NOT_FOUND)
        # endregion

        sid = transaction.savepoint()

        # region lieu verification
        if lieu_data == None:
            return Response({"message": "system can't find 'lieu' in the body of the request"}, status=status.HTTP_400_BAD_REQUEST)
        lieu_data["entreprise"] = organisme_accueil_id
        lieu_serializer = LieuSerializer(data=lieu_data)
        if lieu_serializer.is_valid():
            lieu_serializer.save()
        else:
            return Response(lieu_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # endregion

        # region responsable administratif verification
        if responsable_administratif_data == None:
            transaction.savepoint_rollback(sid)
            return Response({"message": "system can't find 'responsableAdministratif' in the body of the request"}, status=status.HTTP_400_BAD_REQUEST)
        responsable_administratif_data["entreprise"] = organisme_accueil_id
        responsable_administratif_serializer = ResponsableAdministratifSerializer(
            data=responsable_administratif_data)
        if responsable_administratif_serializer.is_valid():
            responsable_administratif_serializer.save()
        else:
            return Response(responsable_administratif_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # endregion

        # region maitre stage verification
        if maitre_stage_data == None:
            transaction.savepoint_rollback(sid)
            return Response({"message": "system can't find 'maitreStage' in the body of the request"}, status=status.HTTP_400_BAD_REQUEST)
        maitre_stage_data["entreprise"] = organisme_accueil_id
        maitre_stage_serializer = MaitreStageSerializer(
            data=maitre_stage_data)
        if maitre_stage_serializer.is_valid():
            maitre_stage_serializer.save()
        else:
            transaction.savepoint_rollback(sid)
            return Response(maitre_stage_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # endregion

        # region proposeur stage verification
        if proposeur_stage_data == None:
            transaction.savepoint_rollback(sid)
            return Response({"message": "system can't find 'proposeurStage' in the body of the request"}, status=status.HTTP_400_BAD_REQUEST)
        proposeur_stage_data["entreprise"] = organisme_accueil_id
        proposeur_stage_serializer = ProposeurStageSerializer(
            data=proposeur_stage_data)
        if proposeur_stage_serializer.is_valid():
            proposeur_stage_serializer.save()
        else:
            transaction.savepoint_rollback(sid)
            return Response(proposeur_stage_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # endregion

        # region mots clé verification
        if list_mot_cle_data == None:
            transaction.savepoint_rollback(sid)
            return Response({"message": "system can't find 'list_mot_cle' in the body of the request"}, status=status.HTTP_400_BAD_REQUEST)

        list_mot_cle = []
        for mot_cle_data in list_mot_cle_data:
            try:
                mot_cle = Mot_cle.objects.get(id=mot_cle_data["id"])
                list_mot_cle.append(mot_cle)
            except Mot_cle.DoesNotExist:
                transaction.savepoint_rollback(sid)
                error_message = f"Mot_cle with id : {mot_cle_data['id']} doesn\'t exist"
                return Response({"message": error_message}, status=status.HTTP_404_NOT_FOUND)

        if len(list_mot_cle) == 0:
            transaction.savepoint_rollback(sid)
            error_message = "list_mot_cle needs to contain at least 1 element (can't be empty)"
            return Response({"message": error_message}, status=status.HTTP_404_NOT_FOUND)

        # endregion

        # region creation stage
        if stage_data == None:
            transaction.savepoint_rollback(sid)
            return Response({"message": "system can't find 'stage' in the body of the request"}, status=status.HTTP_400_BAD_REQUEST)

        stage_data["etudiant"] = etudiant_id
        stage_data["entreprise"] = organisme_accueil_id
        stage_data["representant_etablissement"] = responsable_administratif_serializer.data["id"]
        stage_data["maitre_stage"] = maitre_stage_serializer.data["id"]
        stage_data["lieu"] = lieu_serializer.data["id"]
        stage_data["ayant_propose_stage"] = proposeur_stage_serializer.data["id"]

        stage_serializer = StageCreateSerializer(
            data=stage_data)

        if stage_serializer.is_valid():
            stage_serializer.save()
            stage = Stage.objects.get(id=stage_serializer.data["id"])
            for mot_cle in list_mot_cle:
                stage.list_mot_cle.add(mot_cle)
            serializer = StageSerializer(stage)
            transaction.savepoint_commit(sid)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            transaction.savepoint_rollback(sid)
            return Response(stage_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # endregion
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_stage(request, id):
    if request.method == 'PUT':
        stage_data = request.data

        try:
            stage = Stage.objects.get(id=id)
        except Stage.DoesNotExist:
            error_message = f"Stage with id : {id} doesn\'t exist"
            return Response({"message": error_message}, status=status.HTTP_404_NOT_FOUND)

        stage_data["etat"] = Etat.SUJET_EN_ATTENTE_VALIDATION
        stage_serializer = StageUpdateSerializer(stage,
                                                 data=stage_data)

        if stage_serializer.is_valid():
            stage_serializer.save()
            return Response(stage_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(stage_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def confirme_stage(request, id):
    if request.method == 'PUT':
        etudiant_id = request.query_params.get("etudiantId")
        # njibouh from cookies later

        try:
            stage = Stage.objects.get(id=id)
        except Stage.DoesNotExist:
            error_message = f"Stage with id : {id} doesn\'t exist"
            return Response({"message": error_message}, status=status.HTTP_404_NOT_FOUND)

        stage_serializer = StageConfirmationSerializer(
            stage, data={"etat": Etat.SUJET_CONFIRME, "date_confirmarion": datetime.now()})

        if stage_serializer.is_valid():
            stage_serializer.save()
            Stage.objects.filter(etudiant=etudiant_id, etat__in=[Etat.SUJET_BROUILLON, Etat.SUJET_EN_ATTENTE_VALIDATION, Etat.SUJET_SOUS_REVERVE, Etat.SUJET_VALIDE]).update(
                etat=Etat.SUJET_ABANDONNE)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(stage_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@ api_view(['GET'])
def my_stages(request):
    if request.method == 'GET':
        etat_query = request.query_params.get('etat')
        # njibouh from cookies later
        etudiant_id_query = request.query_params.get('etudiantId')
        entreprise_nom_query = request.query_params.get(
            'organismeAccueilNom')
        filters = {}

        if etat_query:
            filters['etat'] = etat_query
        if etudiant_id_query:
            try:
                Etudiant.objects.get(identifiant=etudiant_id_query)
            except Etudiant.DoesNotExist:
                error_message = f"Etudiant with identifiant : {etudiant_id_query} doesn\'t exist"
                return Response({"message": error_message}, status=status.HTTP_404_NOT_FOUND)

            filters['etudiant__identifiant'] = etudiant_id_query
        else:
            return Response({"message": "system can't find 'etudiantId' in the params of the request"}, status=status.HTTP_400_BAD_REQUEST)

        if entreprise_nom_query:
            filters['entreprise__nom'] = entreprise_nom_query

        list_stage = Stage.objects.filter(**filters).all()

        response = []
        for stage in list_stage:
            list_mot_cle = []
            for mot_cle in stage.list_mot_cle.all():
                list_mot_cle.append(MotCleSerializer(mot_cle).data)
            element = {"stage": StageSerializer(
                stage).data,
                "entreprise": OrganismeAccueilSerializer(stage.entreprise).data,
                "representant_etablissement": ResponsableAdministratifSerializer(stage.representant_etablissement).data,
                "maitre_stage": MaitreStageSerializer(stage.maitre_stage).data,
                "lieu": LieuSerializer(stage.lieu).data,
                "ayant_propose_stage": ProposeurStageSerializer(stage.ayant_propose_stage).data,
                "list_mot_cle": list_mot_cle,
            }
            if stage.tuteur != None:
                element["tuteur"] = TuteurSerializer(stage.tuteur).data
            response.append(element)
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_convention(request, id):
    if request.method == 'GET':
        # njibouh from cookies later
        etudiant_id_query = request.query_params.get('etudiantId')
        try:
            stage = Stage.objects.get(id=id)
        except Stage.DoesNotExist:
            error_message = f"Stage with id : {id} doesn\'t exist"
            return Response({"message": error_message}, status=status.HTTP_404_NOT_FOUND)

        if etudiant_id_query == None or stage.etudiant.identifiant != etudiant_id_query:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        convention = stage.convention.open()
        response = FileResponse(convention)
        return response
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@ api_view(['GET', 'POST', 'PUT'])
def organisme_accueil(request):
    if request.method == 'GET':
        list_organisme_accueil = Organisme_Accueil.objects.all()
        serializer = OrganismeAccueilSerializer(
            list_organisme_accueil, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        organisme_accueil_serializer = OrganismeAccueilSerializer(
            data=request.data)
        if organisme_accueil_serializer.is_valid():
            organisme_accueil_serializer.save()
            return Response(organisme_accueil_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(organisme_accueil_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


"""
 etatQuery = request.query_params.get('etat')
        serviceQuery = request.query_params.get('service')
        siteQuery = request.query_params.get('site')
        filters = {}

        if etatQuery:
            filters['etat'] = etatQuery
        if serviceQuery:
            filters['service'] = serviceQuery

        number_employee_france = Personnel.objects.filter(**filters).count()

        number_employee_chili = db_chili.models.Personnel.objects.using(
            'site_chili').filter(**filters).count()

        number_employee_danemark = db_danemark.models.Personnel.objects.using(
            'site_danemark').filter(**filters).count()

        if siteQuery == None:
            return Response(number_employee_france + number_employee_chili + number_employee_danemark)
        else:
            if siteQuery == "France":
                return Response(number_employee_france)
            elif siteQuery == "Chili":
                return Response(number_employee_chili)
            elif siteQuery == "Danemark":
                return Response(number_employee_danemark)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
"""
