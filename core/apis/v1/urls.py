from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView
from core.apis.v1.viewsets import *


auth_route = routers.DefaultRouter()
auth_route.register(r"register", RegisterViewSet,  basename="register")
auth_route.register(r"login", LoginViewSet,  basename="login")

urlpatterns = [
    path("auth/", include([
        path("", include(auth_route.urls)),
        path("blacklist/", TokenBlacklistView.as_view(), name="token-blacklist"),
        path("refresh/", TokenRefreshView.as_view(), name="token-refresh")
    ])),
    
]