from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('create-memory-game/', MemoryNumView.as_view(), name='create_memorynum'),
    path('get-memory-num/<room_code>', GetMemoryNum.as_view(), name = 'get_memory_num'),
    path('performance/', MemoryPerformanceView.as_view(), name = 'memory_performance'),
    path('performance/<client_id>', MemoryPerformanceView.as_view(), name = 'get_memory_performance') 
]