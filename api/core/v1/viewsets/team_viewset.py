from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.models import Team
from api.core.v1.serializers import TeamSerializer
from api.core.v1.permissions import IsOwner


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
    
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
        
    def create(self, request, *args,  **kwargs):
        
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=request.user)
            
        except:
            return Response(
                {"detail": "Internal Server Error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
    
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    
    @action(methods = ["GET"], detail = True)
    def members(self, request, pk = None):
        return Response({"detail" : "Members"})
    