from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.models import Team, Note
from api.core.v1.serializers import TeamSerializer, JoinTeamSerializer, NoteSerializer
from api.core.v1.permissions import IsOwner
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class TeamViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin, 
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    def get_permissions(self):
        
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwner()]
         
        return super().get_permissions()
    
    
    def get_serializer_class(self):
        
        if self.action == "join":
            return JoinTeamSerializer
        elif self.action == "notes":
            return NoteSerializer
        
        return super().get_serializer_class()
    
    
    @swagger_auto_schema(
        operation_summary="List all teams.",
        operation_description="This endpoint retrieves a list of teams.",
        responses={
            status.HTTP_200_OK: openapi.Response("OK", TeamSerializer(many=True, context = {"exclude_fields" : []})),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response("Internal Server Error"),
        },
    )
    def list(self, request, *args, **kwargs):
        """
        List all teams.

        Returns:
        - List of all teams if successful.
        - Internal Server Error if an unexpected exception occurs.
        """
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"detail" : "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
            
    @swagger_auto_schema(
        operation_summary="Retrieve a team by ID.",
        operation_description="This endpoint retrieve a specific team from the path parameter.",
        responses={
            status.HTTP_200_OK: openapi.Response("OK", TeamSerializer(context = {"exclude_fields" : []})),
            status.HTTP_404_NOT_FOUND: openapi.Response("Team not found"),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response("Internal Server Error"),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a team by ID.

        Returns:
        - Retrieved team details if found.
        - Team not found error if the team does not exist.
        - Internal Server Error if an unexpected exception occurs.
        """
        try:
            return super().retrieve(request, *args, **kwargs)
        except Team.DoesNotExist:
            return Response(
                {"detail" : "Team does not exists."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail" : "Internal Server Error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    
    @swagger_auto_schema(
        operation_summary="Create a new team.",
        operation_description="This endpoint lets you creates a new team",
        responses={
            status.HTTP_201_CREATED: openapi.Response("Created", TeamSerializer(context = {"exclude_fields" : []})),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response("Internal Server Error"),
        },
    )
    def create(self, request, *args,  **kwargs):
        """
        Create a new team.

        Returns:
        - Created team details if successful.
        - Internal Server Error if an unexpected exception occurs.
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=request.user)
            
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            return Response(
                {"detail": "Internal Server Error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    
    @swagger_auto_schema(
        operation_summary="Update a team.",
        operation_description="This endpoint update all the team information based on the body request.",
        responses={
            status.HTTP_200_OK: openapi.Response("OK", TeamSerializer(context = {"exclude_fields" : []})),
            status.HTTP_404_NOT_FOUND: openapi.Response("Team not found"),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response("Internal Server Error"),
        },
    )
    def update(self, request, *args, **kwargs):
        """
        Update a team.

        Returns:
        - Updated team details if successful.
        - Team not found error if the team does not exist.
        - Internal Server Error if an unexpected exception occurs.
        """
        try: 
            return super().update(request, *args, **kwargs)
        except Team.DoesNotExist:
            return Response(
                {"detail" : "Team does not exists."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail" : "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    
    @swagger_auto_schema(
        operation_summary="Partial update of a team.",
        operation_description="This endpoint partially update one or more team information based on the body request.",
        responses={
            status.HTTP_200_OK: openapi.Response("OK", TeamSerializer(context = {"exclude_fields" : []})),
            status.HTTP_404_NOT_FOUND: openapi.Response("Team not found"),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response("Internal Server Error"),
        },
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Partial update of a team.

        Returns:
        - Partially updated team details if successful.
        - Team not found error if the team does not exist.
        - Internal Server Error if an unexpected exception occurs.
        """
        try: 
            return super().partial_update(request, *args, **kwargs)
        except Team.DoesNotExist:
            return Response(
                {"detail" : "Team does not exists."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail" : "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


    @action(methods = ["POST"], detail = True)
    def join(self, request, pk = None):
        try: 
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            team = Team.objects.filter(
                code=serializer.validated_data["code"]).first()

            if team and request.user in team.members.all():
                return Response(
                    {"detail": "User is already a member."},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            team.members.add(request.user)
            
            return Response(
                {"detail": "User successfully added to the team."},
                status=status.HTTP_201_CREATED
            )
            
        except Team.DoesNotExist:
            return Response(
                {"detail": "Team does not exist."}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        except Exception as e:
            return Response( 
                {"detail" : "Internal Server Error"},
                status = status.HTTP_200_OK
            )
    

    @action(methods = ["DELETE"], detail = True)
    def leave(self, request, pk = None):
        try:
            team = self.queryset.filter(id = pk).first()
            
            if team and request.user == team.owner:
                return Response(
                    {"detail" : "User is an owner."},
                    status = status.HTTP_400_BAD_REQUEST
                ) 
            
            if not (team and request.user in team.members.all()):
                return Response(
                    {"detail" : "User is not a member of the team."},
                    status = status.HTTP_400_BAD_REQUEST
                ) 
            
            team.members.remove(request.user)

            return Response(
                {"detail": "User successfully left the team."},
                status=status.HTTP_200_OK
            )
            
        except Team.DoesNotExist:
            return Response(
                {"detail": "Team does not exist."}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        except Exception as e: 
            return Response( 
                {"detail" : "Internal Server Error"},
                status = status.HTTP_200_OK
            )
            
    
    @action(methods=["GET"], detail=True)
    def notes(self, request, pk=None):
        try:
            team = self.get_object()  
            notes = team.notes.all()
            serializer = self.get_serializer(notes, many=True)  
            return Response(serializer.data, status=status.HTTP_200_OK) 
        
        except Team.DoesNotExist:
            return Response(
                {"detail": "Team does not exist."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        except Exception as e: 
            return Response(
                {"detail": "Internal Server Error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )