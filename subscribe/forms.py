from django import forms
from .models import SubscriptionPlan, Subscription

class SubscriptionForm(forms.ModelForm):
    email = forms.EmailField(required=False, help_text="Email for anonymous users")

    class Meta:
        model = Subscription
        fields = ['plan', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plan'].queryset = SubscriptionPlan.objects.all()
        self.fields['plan'].empty_label = "Select a Plan"
        self.fields['plan'].required = True

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        plan = cleaned_data.get("plan")

        if not self.instance.user and not email:
            self.add_error('email', 'Email is required for anonymous users.')

        if not plan:
            self.add_error('plan', 'A subscription plan must be selected.')

        return cleaned_data



class OrderForm(forms.Form):
    full_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    country = forms.CharField(max_length=100, required=True)
    postcode = forms.CharField(max_length=20, required=True)
    town_or_city = forms.CharField(max_length=100, required=True)
    street_address1 = forms.CharField(max_length=100, required=True)
    street_address2 = forms.CharField(max_length=100, required=False)
    county = forms.CharField(max_length=100, required=False)
