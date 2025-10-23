from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_hello_email(email, first_name):
    try:
        send_mail(
            subject="Welcome to our platform!",
            message=f"Hello {first_name},\n\nWelcome to our platform! We're excited to have you on board.\n\nBest regards,\nThe Team",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        logger.info(f"Welcome email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send welcome email to {email}: {e}")
        raise e