from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Subscription, SubscriptionPlan
from datetime import datetime, timedelta
from django.core.mail import send_mail

def subscribe(request):
    plan = SubscriptionPlan.objects.get(name="Basic Plan")  # Example plan
    if request.method == "POST":
        email = request.POST.get('email')
        subscription = Subscription(
            plan=plan,
            start_date=datetime.now().date(),
            end_date=datetime.now().date() + timedelta(days=7),  # 7-day trial
            is_trial=True,
            email=email
        )
        subscription.save()
        # Send confirmation email (if desired)
        send_mail(
            'Subscription Confirmation',
            'Thank you for subscribing to our free trial!',
            'noreply@codenomad.com',
            [email],
            fail_silently=False,
        )
        return redirect('subscription_success')
    return render(request, 'subscribe.html', {'plan': plan})

def subscription_success(request):
    return render(request, 'subscription_success.html')
