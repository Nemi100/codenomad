import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import OrderForm

# Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY

def subscribe(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            # Create a Stripe customer
            customer = stripe.Customer.create(
                email=order_form.cleaned_data['email'],
                name=order_form.cleaned_data['full_name'],
                address={
                    'line1': order_form.cleaned_data['street_address1'],
                    'line2': order_form.cleaned_data['street_address2'],
                    'postal_code': order_form.cleaned_data['postcode'],
                    'city': order_form.cleaned_data['town_or_city'],
                    'state': order_form.cleaned_data['county'],
                    'country': order_form.cleaned_data['country'],
                },
            )

            # Create a Stripe payment intent
            payment_intent = stripe.PaymentIntent.create(
                amount=calculate_amount(request.POST.get('subscription_plan')),
                currency='gbp',
                customer=customer.id,
                description=f"Subscription: {request.POST.get('subscription_plan')}",
                metadata={'order_id': '1234'},
            )

            return JsonResponse({'client_secret': payment_intent['client_secret']})
    else:
        order_form = OrderForm()

    context = {
        'order_form': order_form,
        'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY,
        # Can add client_secret if needed for initial form rendering:
        # 'client_secret': 'initial_client_secret_if_any',
    }

    return render(request, 'subscribe/subscribe.html', context)

def calculate_amount(plan):
    if plan == 'yearly':
        return 40000  # Amount in pence for £400
    else:
        return 3999  # Amount in pence for £39.99
