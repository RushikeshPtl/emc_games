from http import client
from django.db import models

# Create your models here.
class Client(models.Model):
    client_id = models.IntegerField(null= True)
    client_name=models.CharField(max_length=50, null=True)
   
    class Meta:
        db_table = 'Clients'

    def __str__(self):
        return str(self.client_id)