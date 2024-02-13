from django.urls import path, include
from core.apis.v1 import *

urlpatterns = [
    path("v1/", include(api_route_v1))
]