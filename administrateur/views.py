from .serializers import MotCleSerializer, TuteurSerializer, FiliereSerializer, FiliereUpdateSerializer, MotCleUpdateSerializer
from ufr_st.models import Mot_cle, Filiere, Tuteur
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from stage.models import Stage, Etat
from entreprise.models import Organisme_Accueil
# Create your views here.


# region Filiere
@ api_view(['GET', 'POST'])
def get_add_filiere(request):
    if request.method == 'GET':
        list_filiere = Filiere.objects.all()
        serializer = FiliereSerializer(list_filiere, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        filiere_serializer = FiliereSerializer(
            data=request.data)
        if filiere_serializer.is_valid():
            filiere_serializer.save()
            return Response(filiere_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(filiere_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_filiere(request, id):
    if request.method == 'PUT':
        filiere_data = request.data
        try:
            filiere = Filiere.objects.get(identifiant=id)
        except Filiere.DoesNotExist:
            error_message = f"Filiere with identifiant : {id} doesn\'t exist"
            return Response({"message": error_message}, status=status.HTTP_404_NOT_FOUND)

        filiere_serializer = FiliereUpdateSerializer(filiere,
                                                     data=filiere_data)

        if filiere_serializer.is_valid():
            filiere_serializer.save()
            return Response(filiere_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(filiere_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
# endregion


# region Tuteur
@ api_view(['GET', 'POST'])
def get_add_tuteur(request):
    if request.method == 'GET':
        list_tuteur = Tuteur.objects.all()
        serializer = TuteurSerializer(list_tuteur, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        tuteur_serializer = TuteurSerializer(
            data=request.data)
        if tuteur_serializer.is_valid():
            tuteur_serializer.save()
            return Response(tuteur_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(tuteur_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_tuteur(request, id):
    if request.method == 'PUT':
        tuteur_data = request.data

        try:
            tuteur = Tuteur.objects.get(id=id)
        except Tuteur.DoesNotExist:
            error_message = f"Tuteur with id : {id} doesn\'t exist"
            return Response({"message": error_message}, status=status.HTTP_404_NOT_FOUND)

        tuteur_serializer = TuteurSerializer(tuteur,
                                             data=tuteur_data)

        if tuteur_serializer.is_valid():
            tuteur_serializer.save()
            return Response(tuteur_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(tuteur_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
# endregion


# region Mot Cle
@ api_view(['GET', 'POST'])
def get_add_mot_cle(request):
    if request.method == 'GET':
        filiere_query = request.query_params.get(
            'filiere')
        filters = {}

        if filiere_query:
            filters['filiere'] = filiere_query

        list_mot_cle = Mot_cle.objects.filter(**filters).all()

        serializer = MotCleSerializer(list_mot_cle, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        mot_cle_serializer = MotCleSerializer(
            data=request.data)
        if mot_cle_serializer.is_valid():
            mot_cle_serializer.save()
            return Response(mot_cle_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(mot_cle_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_mot_cle(request, id):
    if request.method == 'PUT':
        mot_cle_data = request.data

        try:
            mot_cle = Mot_cle.objects.get(id=id)
        except Mot_cle.DoesNotExist:
            error_message = f"Mot_cle with id : {id} doesn\'t exist"
            return Response({"message": error_message}, status=status.HTTP_404_NOT_FOUND)

        mot_cle_serializer = MotCleUpdateSerializer(mot_cle,
                                                    data=mot_cle_data)

        if mot_cle_serializer.is_valid():
            mot_cle_serializer.save()
            return Response(mot_cle_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(mot_cle_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
# endregion
