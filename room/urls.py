from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('start_game/', StartGame.as_view(), name='start_game'),
    path('start_game/<role>', StartGame.as_view(), name='start_game')
]