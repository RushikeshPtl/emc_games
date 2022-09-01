from typing_extensions import Required
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
from quiz.serializers import *
from memory_game.serializers import *
from img_puzzle.serializers import *

class ClientSerializer(serializers.ModelSerializer):
    quiz_performances = PerformanceSerializer(many=True, read_only=True)
    quiz_results = ResultSerializer(many=True, read_only=True)
    memory_game_numbers = MemoryNumSerializer(many=True, read_only=True)
    memory_game_performances = MemoryPerformanceSerializer(many=True, read_only=True)
    image_puzzle_performance = PuzzlePerformanceSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['client_id', 'client_name', 'quiz_performances','quiz_results','memory_game_numbers','memory_game_performances', 'image_puzzle_performance']