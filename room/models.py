from operator import mod
from pyexpat import model
from django.db import models

# Create your models here.
class Game(models.Model):
    title = models.CharField("title", max_length=100)
    type = models.CharField("type", max_length=100)
    age_group = models.CharField('age_group', max_length=100)

class Room(models.Model):
    room_code = models.IntegerField()
    therapist_id = models.IntegerField()
    client_id = models.IntegerField(null=True)
    is_over = models.BooleanField('is_over', default=False)
    game = models.ForeignKey(Game, on_delete=models.PROTECT)

    class Meta:
        db_table = 'Room'
