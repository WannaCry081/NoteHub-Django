from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import User
from api.core.v1.serializers import UserSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class RegisterViewSet(viewsets.GenericViewSet, 
                   mixins.CreateModelMixin):
    
    serializer_class = UserSerializer


    @swagger_auto_schema(
        operation_summary="Creates the necessary tokens for new users.",
        operation_description="This endpoint creates the refresh and access token for new authenticated users.",
        responses={
            status.HTTP_201_CREATED : openapi.Response("Created", schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "refresh" : openapi.Schema(type=openapi.TYPE_STRING),   
                    "access" : openapi.Schema(type=openapi.TYPE_STRING),   
                }
            )),
            status.HTTP_400_BAD_REQUEST : openapi.Response("Bad Request"),
            status.HTTP_500_INTERNAL_SERVER_ERROR : openapi.Response("Internal Server Error")
        }
    )
    def create(self, request, *args, **kwargs):
        """
        Create method for registering new users.

        This method registers a new user and generates refresh and access tokens for authentication.

        Returns:
        - Refresh and access tokens if successful registration.
        - Bad Request error if the request data is invalid.
        - Internal Server Error if an unexpected exception occurs.
        """
        try:
            serializer = self.get_serializer(data = request.data)
            serializer.is_valid(raise_exception=True)
            
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            
            return Response({
                "refresh" : str(refresh),
                "access" : str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)    
            
        except ValidationError as e:
            return Response(
                {"detail" : str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as e :
            return Response(
                {"detail" : "Internal Server Error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        