from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from core.models import User
from core.apis.v1.serializers import UserSerializer


class RegisterViewSet(viewsets.GenericViewSet, 
                   mixins.CreateModelMixin):
    
    serializer_class = UserSerializer


    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data = request.data)
            serializer.is_valid(raise_exception=True)
            
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            
        except:
            return Response({"detail" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({
            "access" : str(refresh.access_token),
            "refresh" : str(refresh)
        }, status=status.HTTP_201_CREATED)    