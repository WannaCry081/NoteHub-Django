from django.db.models import Q
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.models import User, Team
from api.core.v1.serializers import UserSerializer, TeamSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class UserViewSet(viewsets.GenericViewSet,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    def get_queryset(self):
        """
        Get queryset filtering by current authenticated user.
        """
        return User.objects.filter(id = self.request.user.id)
    
    
    @swagger_auto_schema(
        operation_summary="Gets a specific user.",
        operation_description="This endpoint retrieve a specific authenticated user based on the path parameter `id`.",
        responses={
            status.HTTP_200_OK: openapi.Response("OK", UserSerializer),
            status.HTTP_404_NOT_FOUND: openapi.Response("User not found"),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response("Internal Server Error"),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve method for fetching the details of the authenticated user.

        Returns:
        - User details if found.
        - Not Found error if user not found.
        - Internal Server Error if an unexpected exception occurs.
        """
        try:
            return super().retrieve(request, *args, **kwargs)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": "Internal Server Error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    @swagger_auto_schema(
        operation_summary="Update a specific user information.",
        operation_description="This endpoint updates all the information given to the body request on authenticated specific user.",
        responses={
            status.HTTP_200_OK: openapi.Response("OK", UserSerializer),
            status.HTTP_400_BAD_REQUEST: openapi.Response("Bad Request"),
            status.HTTP_404_NOT_FOUND: openapi.Response("User not found"),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response("Internal Server Error"),
        },
    )
    def update(self, request, *args, **kwargs):
        """
        Update method for updating the details of the authenticated user.

        Returns:
        - Updated user details if successful.
        - Bad Request error if the request data is invalid.
        - Not Found error if user not found.
        - Internal Server Error if an unexpected exception occurs.
        """
        try:
            return super().update(request, *args, **kwargs) 
        except ValidationError as e:
            return Response(
                {"detail": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": "Internal Server Error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    
    @swagger_auto_schema(
        operation_id="Update one or more information about the user",
        operation_description="This endpoint updates one or more information from the body request of a authenticated specific user.",
        responses={
            status.HTTP_200_OK: openapi.Response("OK", UserSerializer),
            status.HTTP_400_BAD_REQUEST: openapi.Response("Bad Request"),
            status.HTTP_404_NOT_FOUND: openapi.Response("User not found"),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response("Internal Server Error"),
        },
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Partial update method for partially updating the details of the authenticated user.

        Returns:
        - Partially updated user details if successful.
        - Bad Request error if the request data is invalid.
        - Not Found error if user not found.
        - Internal Server Error if an unexpected exception occurs.
        """
        try:
            return super().partial_update(request, *args, **kwargs)
        except ValidationError as e:
            return Response(
                {"detail": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": "Internal Server Error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    
    @swagger_auto_schema(
        operation_summary="Delete a specific authenticated user.",
        operation_description="Remove all the information including the specific authenticated user itself.",
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response("No Content"),
            status.HTTP_404_NOT_FOUND: openapi.Response("User not found"),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response("Internal Server Error"),
        },
    )
    def destroy(self, request, *args, **kwargs):
        """
        Destroy method for deleting the authenticated user.

        Returns:
        - No Content if user successfully deleted.
        - Not Found error if user not found.
        - Internal Server Error if an unexpected exception occurs.
        """
        try:
            return super().destroy(request, *args, **kwargs)    
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": "Internal Server Error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        
    @swagger_auto_schema(
        method="GET",
        operation_summary="Lists teams associated with the user.",
        operation_description="This endpoint retrieves all the teams that the specific authenticated user have.",
        responses={
            status.HTTP_200_OK: openapi.Response("OK", TeamSerializer(many=True)),
            status.HTTP_404_NOT_FOUND: openapi.Response("Team not found"),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response("Internal Server Error"),
        },
    )
    @action(methods=["GET"], detail=True)
    def teams(self, request, pk=None):
        try:
            user_teams = Team.objects.filter(
                Q(owner=request.user) | Q(members=request.user))
            
            serializer = TeamSerializer(
                user_teams, 
                many=True,
                context = {"exclude_fields" : ["is_joined"]}) 

            return Response(
                    serializer.data, 
                    status=status.HTTP_200_OK
                )

        except Team.DoesNotExist:
            return Response(
                {"detail" : "Team not found."},
                status = status.HTTP_404_NOT_FOUND
            )
            
        except Exception as e:
            return Response(
                {"detail" : "Internal Server Error"},
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )