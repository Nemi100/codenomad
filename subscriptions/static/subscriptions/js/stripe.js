// static/js/stripe.js

document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded and parsed");

    var stripePublicKeyElement = document.getElementById('id_stripe_public_key');
    var clientSecretElement = document.getElementById('id_client_secret');

    var stripePublicKey = stripePublicKeyElement ? stripePublicKeyElement.textContent.trim() : null;
    var clientSecret = clientSecretElement ? clientSecretElement.textContent.trim() : null;

    console.log("Stripe Public Key:", stripePublicKey);
    console.log("Client Secret Retrieved from Template:", clientSecret);

    if (!stripePublicKey || !clientSecret) {
        console.error("Missing Stripe public key or client secret");
        return;
    }

    var stripe = Stripe(stripePublicKey);
    var elements = stripe.elements();

    var style = {
        base: {
            color: '#000',
            fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
            fontSmoothing: 'antialiased',
            fontSize: '16px',
            '::placeholder': {
                color: '#aab7c4'
            }
        },
        invalid: {
            color: '#dc3545',
            iconColor: '#dc3545'
        }
    };

    var card = elements.create('card', {style: style});
    card.mount('#card-element');
    console.log("Card element mounted");

    card.on('change', function(event) {
        var displayError = document.getElementById('card-errors');
        if (event.error) {
            var html = `
                <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                </span>
                <span>${event.error.message}</span>
            `;
            displayError.innerHTML = html;
        } else {
            displayError.textContent = '';
        }
    });

    var form = document.getElementById('subscription-form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        console.log("Form submitted");

        if (clientSecret) {
            stripe.confirmCardPayment(clientSecret, {
                payment_method: {
                    card: card,
                    billing_details: {
                        name: form.full_name.value,
                        email: form.email.value
                    }
                }
            }).then(function(result) {
                if (result.error) {
                    var errorDiv = document.getElementById('card-errors');
                    var html = `
                        <span class="icon" role="alert">
                        <i class="fas fa-times"></i>
                        </span>
                        <span>${result.error.message}</span>`;
                    errorDiv.innerHTML = html;
                    card.update({ 'disabled': false });
                    document.getElementById('submit-button').removeAttribute('disabled');
                } else {
                    if (result.paymentIntent.status === 'succeeded') {
                        form.submit();
                    }
                }
            });
        } else {
            var errorElement = document.getElementById('card-errors');
            errorElement.textContent = "Client secret is not available. Please try again.";
        }
    });
});