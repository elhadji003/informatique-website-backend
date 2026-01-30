# payments/urls.py
from django.urls import path
from .views import init_payment, payment_callback

# payments/urls.py
urlpatterns = [
    path("init/", init_payment),
    path("callback/", payment_callback), # L'URL sera donc /api/payments/callback/
]
