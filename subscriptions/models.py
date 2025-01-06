from django.db import models
from django.conf import settings

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    subscription_plan = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_trial = models.BooleanField(default=False)

class PaymentIntent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    intent_id = models.CharField(max_length=255)
    amount = models.IntegerField()
    currency = models.CharField(max_length=10)
    status = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

class PaymentTransaction(models.Model):
    intent_id = models.CharField(max_length=255)
    transaction_id = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
