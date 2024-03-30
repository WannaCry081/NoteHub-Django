from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.models import Note, Team
from api.core.v1.serializers import NoteSerializer


class NoteViewSet(viewsets.GenericViewSet, 
                  mixins.CreateModelMixin, 
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    def create(self, request, *args, **kwargs):
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
    
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)