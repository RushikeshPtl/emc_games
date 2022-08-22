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
    user_id = serializers.SerializerMethodField('get_user_id')

    class Meta:
        model = MemoryPerformance
        fields = ('id', 'user_id', 'event_id', 'memory_number','inputnumber', 'is_correct')

    def get_memory_number(self, obj):
        return obj.memorynumber.number

    def get_user_id(self, obj):
        return obj.user_id.user_id
    
    