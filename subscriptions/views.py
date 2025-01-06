from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .forms import SubscriptionForm, PaymentForm
from .models import Subscription, PaymentIntent, PaymentTransaction
import stripe
from datetime import timedelta
from django.utils import timezone

# Stripe configuration
stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription_plan = form.cleaned_data['subscription_plan']

            if request.user.is_authenticated:
                subscription.user = request.user
            else:
                subscription.user = None

            subscription.start_date = timezone.now()
            subscription.end_date = subscription.start_date + timedelta(days=7)
            subscription.is_trial = True
            subscription.save()

            request.session['subscription_id'] = subscription.id
            return redirect('subscriptions:create_payment_intent')
    else:
        form = SubscriptionForm()

    return render(request, 'subscriptions/subscribe.html', {'form': form})

@csrf_exempt
def create_payment_intent(request):
    subscription_id = request.session.get('subscription_id')
    if not subscription_id:
        return redirect('subscriptions:subscribe')

    subscription = Subscription.objects.get(id=subscription_id)
    amount = 3999 if subscription.subscription_plan == 'monthly' else 39900

    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency='gbp',
        metadata={'subscription_id': subscription_id}
    )
    PaymentIntent.objects.create(
        user=subscription.user,
        intent_id=intent['id'],
        amount=amount,
        currency='gbp',
        status=intent['status']
    )

    print("Generated client_secret:", intent['client_secret'])

    return render(request, 'subscriptions/create_payment_intent.html', {
        'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY,
        'client_secret': intent['client_secret'],
        'intent_id': intent['id']
    })

@csrf_exempt
def confirm_payment(request, intent_id):
    intent = stripe.PaymentIntent.retrieve(intent_id)
    if intent.status == 'succeeded':
        PaymentTransaction.objects.create(
            intent_id=intent['id'],
            transaction_id=intent['charges']['data'][0]['id'],
            status=intent['status']
        )
        return redirect('subscriptions:success')

    return render(request, 'subscriptions/confirm_payment.html', {'intent': intent})

def success(request):
    return render(request, 'subscriptions/success.html')
