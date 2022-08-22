from django.db import models

# Create your models here.
class Client(models.Model):
    user_id = models.IntegerField(null= True)
    user_name=models.CharField(max_length=50, null=True)
   
    class Meta:
        db_table = 'Clients'

    def __str__(self):
        return str(self.user_id)