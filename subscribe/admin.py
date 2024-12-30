from django.contrib import admin
from .models import SubscriptionPlan, Subscription, Payment

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration')
    search_fields = ('name',)
    list_filter = ('price', 'duration')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'is_active', 'is_trial', 'email')
    search_fields = ('user__username', 'email', 'plan__name')
    list_filter = ('is_active', 'is_trial', 'plan')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('subscription', 'transaction_id', 'amount', 'payment_date', 'status')
    search_fields = ('transaction_id', 'subscription__user__username', 'subscription__email')
    list_filter = ('status', 'payment_date')
