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
