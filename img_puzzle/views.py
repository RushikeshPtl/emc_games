from json import JSONDecodeError
import string
from django.shortcuts import render
from rest_framework.views import APIView
import sys
from img_puzzle.models import Image, PuzzlePiece
from quiz.serializers import PerformanceSerializer
from .views import *
import pdb
from django.http import JsonResponse
from PIL import Image as IMG
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.parsers import FileUploadParser, MultiPartParser
from .serializers import *
from rest_framework.response import Response
import random

# Create your views here.
def create_pieces(image, pieces):
    img = IMG.open(image.image.file)
    img_width = img.size[0]
    img_height = img.size[1]
    rows = 0
    cols = 0
    d = 1
    divisors = []
    while True:
        if pieces%d == 0:
            if d*d == pieces:
                rows, cols = d, d
                break
            elif len(divisors) > 0:
                if d * divisors[-1] == pieces:
                    if img_width >= img_height:
                        rows, cols = divisors[-1], d
                    else:
                        rows, cols = d, divisors[-1]
                    break
                else:
                    divisors.append(d)
            else:
                divisors.append(d)
        d+=1
    shape = str(rows) + 'x' + str(cols)
    piece_width = img_width/cols
    piece_height = img_height/rows
    pos = 0
    for i in range(rows):
        top = piece_height * i
        bottom = piece_height * (i+1)
        for j in range(cols):
            left = piece_width * j
            right = piece_width * (j+1)
            new_img = img.crop((left, top, right, bottom))
            pos += 1
            name = image.image.name
            name = name.split('/')[1] if '/' in name else name
            img_io = io.BytesIO()
            new_img.save(img_io, format="PNG")
            new_pic = InMemoryUploadedFile(
                img_io,
                'ImageField',
                name.split('.')[0]+'_'+str(pos)+'.png',
                'PNG',
                sys.getsizeof(img_io), None
            )
            puzzlepiece = PuzzlePiece(piece=new_pic, image_id = image.id, position = pos, tile_count = pieces, shape=shape)
            puzzlepiece.save()
    return shape

class CreatePuzzleView(APIView):
    parser_classes = (MultiPartParser, )

    def get(self, request):
        return render(request, 'new_image.html')

    def post(self, request):
        if request.FILES['image']:
            therapist_id = request.data.get('therapist_id')
            client_id = random.randint(11, 18)
            client = Client.objects.get_or_create(client_id=client_id)
            name = request.FILES['image'].name
            img = IMG.open(request.FILES['image'])
            width, height = img.size[0], img.size[1]
            proportion = width/height
            img_resize = img.resize((round(480*proportion), 480))
            img_io = io.BytesIO()
            img_resize.save(img_io, format='PNG')
            name_str = random.choices(string.ascii_letters + string.digits, k=8)
            resized_img = InMemoryUploadedFile(
                img_io,
                'ImageField',
                name.split('.')[0]+'_'+''.join(name_str)+'.png',
                'PNG',
                sys.getsizeof(img_io), None
            )
            image = Image.objects.create(image=resized_img, uploaded_by=therapist_id)
            pieces = request.data.get('pieces')
            shape = create_pieces(image, int(pieces))
            puzzle = ImagePuzzleSerializer(image, context = {'pieces' : int(pieces)}).data
            room_codes = Room.objects.all().values("room_code")
            room_code = random.randint(100000, 999999)
            while room_code in room_codes:
                room_code = random.randint(100000, 999999)
            rm = Room.objects.create(room_code = room_code, therapist_id = therapist_id, client_id = Client.objects.get(client_id = client_id).id)
            room = PuzzleRoom.objects.create(room=rm, image=image, shape=shape)
            context = {'image_id' : image.id, 'image_path' : image.image.path, 'image_url' : image.image.url, 'rows' : shape.split('x')[0], 'columns' : shape.split('x')[1], 'room_code' : room_code, 'puzzle_room' : room.id, 'therapist_id' : therapist_id, 'client_id' : client_id, 'role' : 'therapist'}
            return render(request, 'puzzle.html', context=context)
        else:
            return JsonResponse({"MSG":"Please select an Image"})

class GetPuzzleView(APIView):

    def get(self, request, id):
        if id:
            pieces = int(request.query_params.get('pieces'))
            image = Image.objects.get(pk=id)
            if image and image.puzzlepiece_set.filter(tile_count = pieces).count() == pieces:
                image_data = ImagePuzzleSerializer(image, context={'pieces' : pieces}).data
                return Response(image_data)
            else:
                JsonResponse({"MSG" : "Puzzle Not Available"})
        else:
            JsonResponse({"MSG" : "Please Provide Valid Image ID"})

class GetPuzzleRoom(APIView):

    def get(self, request, id):
        if id:
            puzzle_room = PuzzleRoom.objects.get(pk=id)
            room_code = puzzle_room.room.room_code
            therapist_id = puzzle_room.room.therapist_id
            client_id = puzzle_room.room.client.client_id
            image = puzzle_room.image
            shape = puzzle_room.shape
            puzzle = ImagePuzzleSerializer(image, context = {'shape' : shape}).data
            context = {'image_id' : image.id, 'image_path' : image.image.path, 'image_url' : image.image.url, 'rows' : shape.split('x')[0], 'columns' : shape.split('x')[1], 'room_code' : room_code, 'puzzle_room' : id, 'therapist_id' : therapist_id, 'client_id' : client_id, 'role' : 'client'}
            return render(request, 'puzzle.html', context=context)
        else:
            JsonResponse({"MSG" : "Please Provide Valid Puzzle Room ID"})

class PerformanceView(APIView):

    def post(self, request):
        puzzle_room_id = request.data.get('puzzle_room_id')
        client_id = request.data.get('client_id')
        time_taken = request.data.get('time_taken')
        time_over = request.data.get('time_over')
        is_correct = request.data.get('is_correct')
        puzzle_room = PuzzleRoom.objects.get(pk=puzzle_room_id)
        client = Client.objects.get(client_id=client_id)
        performance = PuzzlePerformance.objects.create(puzzleroom = puzzle_room, client = client, time_taken = time_taken, time_over = time_over, is_correct = is_correct)
        performance_data = PerformanceSerializer(performance).data
        return Response(performance_data)
