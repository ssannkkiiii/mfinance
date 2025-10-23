from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from apps.users.tasks.send_hello_email import send_hello_email

User = get_user_model()

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        try:
            send_hello_email.delay(instance.email, instance.first_name or 'User')
        except Exception as e:
            pass
