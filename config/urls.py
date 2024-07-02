"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import os
from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from dotenv import load_dotenv


load_dotenv()

ENVIRONMENT: str = str(os.environ.get("DJANGO_ENV")).lower()

schema_view = get_schema_view(
    openapi.Info(
        title="NoteHub - API",
        default_version="v1",
        description="A Note App Application Programming Interface (API) that provides a user-team experience.",
    ),
    public=True,
    authentication_classes=(JWTAuthentication,),
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path("api/", include([path("v1/", include("api.v1.urls"))])),
]

if ENVIRONMENT == "development":
    urlpatterns += [
        path("admin/", admin.site.urls),
        path("swagger<format>/", schema_view.without_ui(), name="schema-json"),
        path("swagger/", schema_view.with_ui("swagger"), name="schema-redoc"),
        path("redoc/", schema_view.with_ui("redoc"), name="schema-redoc"),
    ]
