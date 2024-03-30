from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import User
from api.core.v1.serializers import UserSerializer


class RegisterViewSet(viewsets.GenericViewSet, 
                   mixins.CreateModelMixin):
    
    serializer_class = UserSerializer


    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data = request.data)
            serializer.is_valid(raise_exception=True)
            
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            
            return Response({
                "refresh" : str(refresh),
                "access" : str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)    
            
        except Exception as e :
            return Response({"detail" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        