from django.shortcuts import render, redirect
from .forms import SubscriptionForm
from .models import SubscriptionPlan, Subscription
from datetime import datetime, timedelta
from django.core.mail import send_mail

def subscribe(request):
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.start_date = datetime.now().date()
            subscription.end_date = datetime.now().date() + timedelta(days=7)  # 7-day trial
            subscription.is_trial = True
            subscription.save()
            # Send confirmation email
            recipient_list = [subscription.email] if subscription.email else [subscription.user.email]
            send_mail(
                'Subscription Confirmation',
                'Thank you for subscribing to our free trial!',
                'noreply@codenomad.com',
                recipient_list,
                fail_silently=False,
            )
            return redirect('subscription_success')
    else:
        form = SubscriptionForm()
    return render(request, 'subscribe.html', {'form': form})

def subscription_success(request):
    return render(request, 'subscription_success.html')
