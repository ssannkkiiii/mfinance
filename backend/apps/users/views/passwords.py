from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from apps.users.models import User
from apps.users.serializers.passwords import UserPasswordChangeSerializer, PasswordResetSerializer
from apps.users.utils.generate_otp import clear_verification

class UserPasswordChangeView(generics.UpdateAPIView):
    serializer_class = UserPasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            
            user = self.get_object()
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            clear_verification(user.email, 'change')
            
            return Response({
                'success': True,
                'message': 'Password changed successfully'
            })
        except ValidationError as e:
            return Response({
                'success': False,
                'message': 'Validation error',
                'errors': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Password change failed',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['new_password']
            
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            
            clear_verification(email, 'reset')
            
            return Response({
                'success': True,
                'message': 'Password reset successfully'
            })
            
        except ValidationError as e:
            return Response({
                'success': False,
                'message': 'Validation error',
                'errors': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': 'User with this email does not exist'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Password reset failed',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)