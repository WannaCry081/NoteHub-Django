from django.contrib.auth import authenticate
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from api.models import User
from api.core.v1.serializers import LoginSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class LoginViewSet(viewsets.GenericViewSet, 
                   mixins.CreateModelMixin):
    
    serializer_class = LoginSerializer

    
    @swagger_auto_schema(
        operation_summary="Creates the necessary tokens for unauthenticated user.",
        operation_description="This endpoint return the newly created refresh and access token for existing unauthenticated user.",
        responses={
            status.HTTP_201_CREATED : openapi.Response("Ok", schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "refresh" : openapi.Schema(type=openapi.TYPE_STRING),   
                    "access" : openapi.Schema(type=openapi.TYPE_STRING),   
                }
            )),
            status.HTTP_401_UNAUTHORIZED : openapi.Response("Unauthorized"),
            status.HTTP_500_INTERNAL_SERVER_ERROR : openapi.Response("Internal Server Error")
        },
    )
    def create(self, request, *args, **kwargs):
        """
        Create method for generating tokens.

        This method creates refresh and access tokens for an existing unauthenticated user based on the provided data.
        
        Returns:
        - Refresh and access tokens if successful.
        - Unauthorized error if invalid credentials.
        - Internal Server Error if an unexpected exception occurs.
        """
        try:
            serializer = self.get_serializer(data = request.data)
            serializer.is_valid(raise_exception = True)

            user = serializer.validated_data.get("user")
            if not user:
                return Response({"detail" : "Invalid credentials. Please try again."}, status=status.HTTP_401_UNAUTHORIZED)
            
            refresh = RefreshToken.for_user(user) 
            
            return Response({
                "refresh" : str(refresh),
                "access" : str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        
        except AuthenticationFailed as e:
            return Response(
                {"detail": str(e)}, 
                status=status.HTTP_401_UNAUTHORIZED
            ) 
        
        except Exception as e:
            return Response(
                {"detail" : "Internal Server Error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        
    
    