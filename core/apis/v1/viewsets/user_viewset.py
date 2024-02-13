from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from core.models import User
from core.apis.v1.serializers import UserSerializer


class UserViewSet(viewsets.GenericViewSet, 
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    def list(self, request, *args, **kwargs):
        
        try:
            queryset = self.filter_queryset(request.user)
            serializer = self.get_serializer(queryset)
            
        except:
            return Response({"detail" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.data, status=status.HTTP_200_OK)