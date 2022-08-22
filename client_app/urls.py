from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [   
    path('get-client-performance/<client_id>', ClientPerformanceView.as_view(), name = 'get_client_performance') 
]