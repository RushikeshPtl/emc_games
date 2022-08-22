from django.shortcuts import render
from rest_framework.response import Response
from .models import *
from rest_framework.views import APIView
from django.http import JsonResponse
from django.core import serializers as sr
import pdb
from .serializers import *

# Create your views here.


class ClientPerformanceView(APIView):
    
    def get(self, request, client_id):
        if client_id:
            cPerformance = Client.objects.filter(client_id = client_id)
            if cPerformance:                
                client_performance_data = ClientSerializer(cPerformance, many = True)
                context = {"performance" : client_performance_data.data}
                return Response(context)
            else:
                return Response("Invalide client id...")
        else:
            return Response("Invalide client id...")
