from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from apps.users.serializers.otp_serializers import OTPRequestSerializer, OTPVerificationSerializer
from apps.users.utils.generate_otp import generate_otp, store_otp, verify_otp
from apps.users.tasks.send_otp_email import send_otp_email
import logging

logger = logging.getLogger(__name__)

class OTPRequestView(generics.GenericAPIView):
    serializer_class = OTPRequestSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            email = serializer.validated_data['email']
            action = serializer.validated_data['action']
            
            otp = generate_otp()
            store_otp(email, action, otp)
            
            try:
                task = send_otp_email.delay(email, otp, action)
                logger.info(f"OTP email task queued for {email} with task ID: {task.id}")
            except Exception as celery_error:
                logger.error(f"Celery failed: {celery_error}, fallback to sync send")
                try:
                    send_mail(
                        subject=f"Verification code for {action}",
                        message=f"Your verification code: {otp}\n\nThis code is valid for 5 minutes.",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[email],
                        fail_silently=False,
                    )
                    logger.info(f"OTP email sent synchronously to {email}")
                except Exception as email_error:
                    logger.error(f"Failed to send OTP email: {email_error}")
                    return Response({
                        'success': False,
                        'message': 'Failed to send OTP email',
                        'error': str(email_error)
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
            return Response({
                'success': True,
                'message': 'OTP code sent to your email'
            })
            
        except ValidationError as e:
            logger.error(f"Validation error in OTP request: {e.detail}")
            return Response({
                'success': False,
                'message': 'Validation error',
                'errors': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in OTP request: {str(e)}")
            return Response({
                'success': False,
                'message': 'Failed to process OTP request',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OTPVerificationView(generics.GenericAPIView):
    serializer_class = OTPVerificationSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            email = serializer.validated_data['email']
            action = serializer.validated_data['action']
            otp = serializer.validated_data['otp']
            
            if verify_otp(email, action, otp):
                logger.info(f"OTP verified successfully for {email}")
                return Response({
                    'success': True,
                    'message': 'OTP verified successfully'
                })
            else:
                logger.warning(f"Invalid OTP for {email}")
                return Response({
                    'success': False,
                    'message': 'Invalid or expired OTP code'
                }, status=status.HTTP_400_BAD_REQUEST)
            
        except ValidationError as e:
            logger.error(f"Validation error in OTP verification: {e.detail}")
            return Response({
                'success': False,
                'message': 'Validation error',
                'errors': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in OTP verification: {str(e)}")
            return Response({
                'success': False,
                'message': 'OTP verification failed',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)