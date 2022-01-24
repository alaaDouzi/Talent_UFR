from datetime import datetime
from rest_framework import status
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ufr_st.models import Mot_cle, Filiere, Tuteur
# Create your views here.
