from distutils.command import upload
from turtle import position
from django.db import models
from client_app.models import Client
from room.models import Room

# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to = 'images')
    uploaded_by = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Images'
    
    def get_pieces(self):
        return self.puzzlepiece_set.all()

class PuzzlePiece(models.Model):
    piece = models.ImageField(upload_to = 'pieces')
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    tile_count = models.IntegerField()
    position = models.IntegerField()
    shape = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'Pieces'

class PuzzleRoom(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    event_id = models.IntegerField(null=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    shape = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'PuzzleRoom'

