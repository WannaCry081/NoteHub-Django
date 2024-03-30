from django.db.models import Q
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
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
    
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs) 
    
    
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)    
    
    
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
        
    
    @action(methods=["GET"], detail=True)
    def notes(self, request, pk=None):
        return Response({"detail" : "Notes"})