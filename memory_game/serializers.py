from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *

class MemoryNumSerializer(ModelSerializer):
    class Meta:
        model = MemoryNum
        fields = '__all__'


class MemoryRoomSerializer(ModelSerializer):   

    class Meta:
        model = MemoryRoom
        fields = '__all__'


class MemoryPerformanceSerializer(ModelSerializer):    
    memory_number = serializers.SerializerMethodField('get_memory_number')
    client = serializers.SerializerMethodField('get_client')

    class Meta:
        model = MemoryPerformance
        fields = ('id', 'client', 'event_id', 'memory_number','inputnumber', 'is_correct')

    def get_memory_number(self, obj):
        return obj.memorynumber.number

    def get_client(self, obj):
        return obj.client.client_id
    
    