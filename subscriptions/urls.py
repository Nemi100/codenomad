from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('subscribe/', views.subscribe, name='subscribe'),
    path('create_payment_intent/', views.create_payment_intent, name='create_payment_intent'),
    path('confirm_payment/<str:intent_id>/', views.confirm_payment, name='confirm_payment'),
    path('success/', views.success, name='success'),
]
