from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import User
from api.core.v1.serializers import LoginSerializer
from django.contrib.auth import authenticate


class LoginViewSet(viewsets.GenericViewSet, 
                   mixins.CreateModelMixin):
    
    serializer_class = LoginSerializer

    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data = request.data)
            serializer.is_valid(raise_exception = True)

            user = serializer.validated_data.get("user")
            if not user:
                return Response({"detail" : "Invalid credentials. Please try again."}, status=status.HTTP_401_UNAUTHORIZED)
            
            refresh = RefreshToken.for_user(user) 
            
            return Response({
                "refresh" : str(refresh),
                "access" : str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"detail" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    
    