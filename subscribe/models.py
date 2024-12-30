import uuid
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class SubscriptionPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(help_text="Duration in days")
    features = models.TextField(blank=True, help_text="Special features of the plan")

    def __str__(self):
        return self.name

class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    is_trial = models.BooleanField(default=False)
    email = models.EmailField(blank=True, help_text="Email for anonymous users")

    def save(self, *args, **kwargs):
        if not self.id and self.is_trial:
            self.start_date = datetime.now().date()
            self.end_date = self.start_date + timedelta(days=7)  # 7-day free trial
        super(Subscription, self).save(*args, **kwargs)

    def __str__(self):
        if self.user:
            return f"{self.user.username} - {self.plan.name}"
        else:
            return f"Anonymous - {self.plan.name}"

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')])

    def __str__(self):
        return f"{self.transaction_id} - {self.status}"
