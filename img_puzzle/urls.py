from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('new-image-puzzle/', CreatePuzzleView.as_view(), name='create_puzzle'),
    path('get-puzzle/<id>', GetPuzzleView.as_view(), name='get_puzzle')
]