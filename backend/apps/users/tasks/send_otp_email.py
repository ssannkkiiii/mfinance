from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_otp_email(email, otp, operation_type):
    try:
        send_mail(
            subject=f"Verification code for {operation_type}",
            message=f"Your verification code: {otp}\n\nCode lifetime 5 minutes.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        logger.info(f"OTP email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send OTP email to {email}: {e}")
        raise e
