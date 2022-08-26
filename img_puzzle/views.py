from json import JSONDecodeError
from django.shortcuts import render
from rest_framework.views import APIView
import sys
from img_puzzle.models import Image, PuzzlePiece
from .views import *
import pdb
from django.http import JsonResponse
from PIL import Image as IMG
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.parsers import FileUploadParser, MultiPartParser
from .serializers import *
from rest_framework.response import Response

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
            shape = str(rows) + 'x' + str(cols)
            puzzlepiece = PuzzlePiece(piece=new_pic, image_id = image.id, position = pos, tile_count = pieces, shape=shape)
            puzzlepiece.save()



class CreatePuzzleView(APIView):
    parser_classes = (MultiPartParser, )

    def get(self, request):
        return render(request, 'new_image.html')

    def post(self, request):
        if request.FILES['image']:
            image = Image.objects.create(image=request.FILES['image'], uploaded_by=request.POST.get('therapist_id'))
            pieces = request.POST.get('pieces')
            create_pieces(image, int(pieces))
            puzzle = ImagePuzzleSerializer(image, context = {'pieces' : int(pieces)}).data
            return Response(puzzle)
        else:
            return JsonResponse({"MSG":"Please select Image"})


class GetPuzzleView(APIView):

    def get(self, request, id):
        if id:
            pieces = request.data.get('pieces')
            image = Image.objects.get(pk=id)
            if image and image.get_pieces.filter(tile_count = pieces).count == pieces:
                image_data = ImagePuzzleSerializer(image, context={'pieces' : pieces}).data
                return Response(image_data)
            else:
                JsonResponse({"MSG" : "Puzzle Not Available"})
        else:
            JsonResponse({"MSG" : "Please Provide Valid Image ID"})


