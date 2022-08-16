from http import client
from multiprocessing import context
from django.shortcuts import render
from ast import While
import json
from urllib import response
from django.shortcuts import render
from rest_framework.response import Response
from .models import *
from rest_framework.views import APIView, View
from django.http import JsonResponse
from django.core import serializers as sr
import pdb
from .serializers import *
import random
from random import randint
from room.models import Room
from django.http import HttpResponse

# Create your views here.
class MemoryNumView(APIView):
    def get(self, request):
        return render(request, 'create_memorynum.html')

    def post(self, request):  
        try:      
            drange=request.POST.get('range')
            therapist_id = request.POST.get('therapist_id')
            client_id = request.POST.get('client_id')
            category = request.POST.get('inlineRadioOptions')
            number=random_with_N_digits(int(drange))
            memoryGame = MemoryNum(
                category = category,
                numberdigit = drange,
                number = number,
                therapist_id = therapist_id,
                client_id = client_id
            )
            memoryGame.save()
            MemoryNum_data = MemoryNumSerializer(memoryGame)
            # return Response(MemoryNum_data.data)
            speed=None
            if category=="easy":
                speed=2500
            elif category=="medium":
                speed=2000
            elif category=="hard":
                speed=1000
            else:
                speed=500
            room_codes = Room.objects.all().values('room_code')
            room_code = random.randint(100000, 999999)
            while room_code in room_codes:
                room_code = random.randint(100000, 999999)
            room = Room.objects.create(room_code = room_code, therapist_id = therapist_id, client_id = client_id)
            memory_room = MemoryRoom.objects.create(room_id = room.id, memorynum = memoryGame)
            context={"number":number, "therapist_id":therapist_id,"client_id":client_id,"speed":speed, "room_code" : room_code, "role" : "Therapist"}
            return render(request, 'memorynum.html', context=context)
        except Exception as e:
            print(e)            
            return Response(status=400)

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

class GetMemoryNum(APIView):
    def get(self, request, room_code):
        if room_code:
            room = Room.objects.filter(room_code = room_code).first()
            if room:
                memory_room = MemoryRoom.objects.filter(room_id = room.id).first()
                number = memory_room.memorynum.number
                category = memory_room.memorynum.category               
                therapist_id = memory_room.memorynum.therapist_id
                client_id = memory_room.memorynum.client_id
                speed=None
                if category=="easy":
                    speed=2500
                elif category=="medium":
                    speed=2000
                elif category=="hard":
                    speed=1000
                else:
                    speed=500               
                context = {"number" : number, "room_code" : room_code, "role" : "Client", "therapist_id":therapist_id,"client_id":client_id,"speed":speed}
                return render(request, 'memorynum.html', context=context)
            else:
                return Response('Room not found.....................')
        else:
            return Response('Please provide valid room code.........')

class MemoryPerformanceView(APIView):
    def post(self,request):
        client_id=request.POST.get('client_id')
        inputnum=request.POST.get('inputnum')
        memoryroom=request.POST.get('room_code')
        event_id=request.POST.get('event_id')

        memorynum=MemoryNum.objects.filter(number=inputnum,client_id=client_id)

        if memorynum:
            mPerformance=MemoryPerformance.objects.create(user_id=client_id,event_id=event_id,memoryroom=memoryroom,memorynum=inputnum,is_correct=True)
        else:
            mPerformance=MemoryPerformance.objects.create(user_id=client_id,event_id=event_id,memoryroom=memoryroom,memorynum=inputnum,is_correct=False)

        memory_performance_data = MemoryPerformanceSerializer(mPerformance, many = True)

        context = {"mPerformance" : memory_performance_data.data}
        return Response(context)

    def get(self, request, client_id):
        if client_id:
            user_id = request.data.get("User ID")
            event_id = request.data.get("Event ID")
            mPerformance = MemoryPerformance.objects.filter(client_id = user_id, event_id = event_id)            
            correct_answers = mPerformance.filter(is_correct = True).count()
            memory_performance_data = MemoryPerformanceSerializer(mPerformance, many = True)
            context = {"performance" : memory_performance_data.data, "correct_answers" : correct_answers}
            return Response(context)
        else:
            return Response("Invalide client id...")
