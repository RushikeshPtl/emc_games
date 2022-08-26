from dataclasses import fields
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
import pdb

class PieceSerializer(ModelSerializer):
    piece_path = serializers.SerializerMethodField('get_piece_path')
    piece_url = serializers.SerializerMethodField('get_piece_url')

    class Meta:
        model = PuzzlePiece
        fields = ('id', 'piece_path', 'piece_url', 'tile_count', 'position', 'shape')
    
    def get_piece_path(self, obj):
        return obj.piece.path
    
    def get_piece_url(self, obj):
        return obj.piece.url

class ImagePuzzleSerializer(ModelSerializer):
    puzzle_pieces = serializers.SerializerMethodField('get_puzzle_pieces')
    image_path = serializers.SerializerMethodField('get_image_path')
    image_url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = Image
        fields = ('id', 'image_path', 'image_url', 'uploaded_by', 'puzzle_pieces')
    
    def get_puzzle_pieces(self, obj):
        pieces = self.context.get('pieces')
        if pieces:
            return PieceSerializer(obj.puzzlepiece_set.filter(tile_count = pieces).order_by('?'), many = True).data
        else:
            return PieceSerializer(obj.get_pieces().order_by('?'), many = True).data
    
    def get_image_path(self, obj):
        return obj.image.path
    
    def get_image_url(self, obj):
        return obj.image.url
    
