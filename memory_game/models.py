from django.db import models
from room.models import Room
# Create your models here.


class MemoryNum(models.Model):    
    category = models.CharField(max_length=100)
    number = models.CharField(max_length=10)
    numberdigit = models.IntegerField()
    therapist_id = models.IntegerField()
    client_id = models.IntegerField(default="0")
    # no_of_questions = models.IntegerField()
    class Meta:
        db_table = 'MemoryNums'
    
    def get_numbers(self):
        return self.number_set.all()

    def __str__(self):
        return str(self.number) 

class MemoryPerformance(models.Model):
    user_id = models.IntegerField()
    event_id = models.IntegerField()    
    memoryroom = models.ForeignKey('MemoryRoom', null=True, on_delete=models.CASCADE)    
    memorynumber = models.ForeignKey('MemoryNum', null=True, on_delete=models.CASCADE)
    inputnum = models.CharField(max_length=100, null=True)
    is_correct = models.BooleanField()

    class Meta:
        db_table = 'MemoryPerformances'

    def __str__(self):
        return str(self.user_id)


class MemoryRoom(models.Model):
    room = models.ForeignKey(Room,null=True, on_delete=models.CASCADE)    
    memorynum = models.ForeignKey(MemoryNum, on_delete=models.CASCADE,null=True)
    event_id = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'MemoryRoom'
    
    def __str__(self):
        return str(self.room)