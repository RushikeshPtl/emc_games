from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from rest_framework.response import Response
import pdb
from rest_framework.views import APIView
from django.views.decorators.clickjacking import xframe_options_sameorigin
# Create your views here.
class StartGame(APIView):

    @xframe_options_sameorigin
    def get(self, request, role):
        return render(request, role+'.html')

    @xframe_options_sameorigin
    def post(self, request):
        event_id = request.data.get('Event ID')
        therapist_id = request.data.get('Therapist ID')
        client_id = request.data.get('Client ID')
        game_id = request.data.get('Game ID')
        
        if therapist_id:
            room = Room.objects.create(room_code = event_id, therapist_id = therapist_id, game_id = game_id)
            game = room.game.title
            context = {'room_code' : event_id , 'username' : 'therapist', 'user_id' : therapist_id, 'role' : 'Therapist'}
            return render(request, game + '.html' , context)
        else:
            room = Room.objects.filter(room_code = event_id, game_id = game_id).first()
            game = room.game.title
            room.client_id = client_id
            room.save()
            context = {'room_code' : event_id , 'username' : 'client', 'user_id' : client_id, 'role' : 'Client'}
            return render(request, game + '.html' , context)
