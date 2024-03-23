from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView
from api.core.v1.viewsets import *


auth_route = routers.DefaultRouter()
auth_route.register(r"register", RegisterViewSet,  basename="register")
auth_route.register(r"login", LoginViewSet,  basename="login")

route = routers.DefaultRouter()
route.register(r"users", UserViewSet, basename="users")
route.register(r"teams", TeamViewSet, basename="teams")
route.register(r"notes", NoteViewSet, basename="notes")

urlpatterns = [
    path("auth/", include([
        path("", include(auth_route.urls)),
        path("blacklist/", TokenBlacklistView.as_view(), name="token-blacklist"),
        path("refresh/", TokenRefreshView.as_view(), name="token-refresh")
    ])),
    
    path("", include(route.urls))
]