from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.models import Note, Team
from api.core.v1.serializers import NoteSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class NoteViewSet(viewsets.GenericViewSet, 
                  mixins.CreateModelMixin, 
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    @swagger_auto_schema(
        operation_summary="Create a new note from the team.",
        operation_description="This endpoint creates a new note associated with the authenticated user and a team.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING),
                "content": openapi.Schema(type=openapi.TYPE_STRING),
                "team": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        responses={
            status.HTTP_201_CREATED: openapi.Response("Created", NoteSerializer),
            status.HTTP_400_BAD_REQUEST: openapi.Response("Bad Request"),
            status.HTTP_404_NOT_FOUND: openapi.Response("Team not found"),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response("Internal Server Error"),
        },
    )
    def create(self, request, *args, **kwargs):
        """
        Create method for creating a new note.

        This endpoint creates a new note associated with the authenticated user and a team.

        Returns:
        - Created note details if successful.
        - Bad Request error if the request data is invalid.
        - Team not found error if the specified team does not exist.
        - Internal Server Error if an unexpected exception occurs.
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=request.user)
            
            note = serializer.instance 
            
            team = Team.objects.get(id=request.data["team"])
            team.notes.add(note)
            
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return Response(
                {"detail" : str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Team.DoesNotExist:
            return Response(
                {"detail" : "Team not found."},
                status = status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": "Internal Server Error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    
    @swagger_auto_schema(
        operation_summary="Retrieve a note from the team.",
        operation_description="This endpoint gets a specific note from the specific team.",
        responses={
            status.HTTP_200_OK: openapi.Response("OK", NoteSerializer),
            status.HTTP_404_NOT_FOUND: openapi.Response("Note not found"),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response("Internal Server Error"),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve method for retrieving a note.

        Returns:
        - Retrieved note details if found.
        - Note not found error if the note does not exist.
        - Internal Server Error if an unexpected exception occurs.
        """
        return super().retrieve(request, *args, **kwargs)
    
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)