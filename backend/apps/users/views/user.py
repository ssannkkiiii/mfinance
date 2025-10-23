from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from apps.users.models import User
from apps.users.serializers.user import UserSerializer, UserUpdateSerializer, UserOwnSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        if self.action == 'list':
            return User.objects.filter(is_active=True)
        return User.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to retrieve users',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to retrieve user',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class UserOwnView(generics.RetrieveUpdateAPIView):
    serializer_class = UserOwnSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to retrieve user',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Failed to update user',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)