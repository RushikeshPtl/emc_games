from operator import mod
from pyexpat import model
from django.db import models
from client_app.models import *

# Create your models here.
class Game(models.Model):
    title = models.CharField("title", max_length=100)
    type = models.CharField("type", max_length=100)
    age_group = models.CharField('age_group', max_length=100)

    def __str__(self):
        return self.title+"|"+self.type+"|"+self.age_group
    

class Room(models.Model):
    room_code = models.IntegerField()
    therapist_id = models.IntegerField()
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, null=True) 
    is_over = models.BooleanField('is_over', default=False)
    game = models.ForeignKey(Game, on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = 'Room'

    def __str__(self):
        return str(self.room_code)
