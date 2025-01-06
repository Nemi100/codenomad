from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from .models import Subscription

class SubscriptionForm(forms.ModelForm):
    PLAN_CHOICES = [
        ('monthly', 'Monthly - £39.99'),
        ('yearly', 'Yearly - £399.99'),
    ]

    subscription_plan = forms.ChoiceField(choices=PLAN_CHOICES, label="Subscription Plan")
    full_name = forms.CharField(max_length=255, label="Full Name", widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    email = forms.EmailField(label="Email Address", widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))
    house_number = forms.CharField(max_length=10, label="House Number", widget=forms.TextInput(attrs={'placeholder': 'House Number'}))
    street = forms.CharField(max_length=255, label="Street", widget=forms.TextInput(attrs={'placeholder': 'Street'}))
    city = forms.CharField(max_length=255, label="City", widget=forms.TextInput(attrs={'placeholder': 'City'}))
    postcode = forms.CharField(max_length=10, label="Postcode", widget=forms.TextInput(attrs={'placeholder': 'Postcode'}))

    class Meta:
        model = Subscription
        fields = ['subscription_plan', 'full_name', 'email', 'house_number', 'street', 'city', 'postcode']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'subscription_plan',
            'full_name',
            'email',
            Row(
                Column('house_number', css_class='form-group col-md-4'),
                Column('street', css_class='form-group col-md-4'),
                Column('city', css_class='form-group col-md-4'),
                Column('postcode', css_class='form-group col-md-4'),
                css_class='form-row'
            ),
            HTML('<div class="alert alert-info mt-3"><p>Your subscription includes a 7-day free trial. After the trial period, the chosen plan fee will be charged.</p></div>'),
            HTML('<div id="card-element"></div>'),  # Placeholder for Stripe JS
            HTML('<div id="card-errors" role="alert" class="mb-3 text-danger"></div>'),
            Submit('submit', 'Continue to Payment', css_class='btn btn-black rounded-0')
        )

class PaymentForm(forms.Form):
    # Define any additional fields needed for the payment form here
    pass
