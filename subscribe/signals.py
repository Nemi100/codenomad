from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Subscription

@receiver(post_save, sender=Subscription)
def send_subscription_confirmation(sender, instance, created, **kwargs):
    if created:
        subject = "Subscription Confirmation"
        message = "Thank you for subscribing to our free trial!"
        recipient_list = [instance.email] if instance.email else [instance.user.email]
        send_mail(
            subject,
            message,
            'noreply@codenomad.com',
            recipient_list,
            fail_silently=False,
        )

@receiver(post_delete, sender=Subscription)
def log_subscription_deletion(sender, instance, **kwargs):
    print(f"Subscription for {instance} has been deleted.")
