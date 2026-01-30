import requests
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Payment
from rest_framework.permissions import AllowAny
from django.utils import timezone
from datetime import timedelta

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def init_payment(request):
    user = request.user
    amount = request.data.get("amount")
    plan_type = request.data.get("plan_type")

    payload = {
        "invoice": {
            "total_amount": amount,
            "description": f"Abonnement {plan_type} - Lear Informatique"
        },
        "store": { "name": "Lear Informatique" },
        "actions": {
            "return_url": "http://localhost:5173/payment-success", # Ton port Vite est 5173
            "cancel_url": "http://localhost:5173/dashboard",
        },
        "custom_data": { "user_id": user.id }
    }

    headers = {
        "Content-Type": "application/json",
        "PAYDUNYA-MASTER-KEY": settings.PAYDUNYA_MASTER_KEY,
        "PAYDUNYA-PRIVATE-KEY": settings.PAYDUNYA_PRIVATE_KEY,
        "PAYDUNYA-PUBLIC-KEY": settings.PAYDUNYA_PUBLIC_KEY,
        "PAYDUNYA-TOKEN": settings.PAYDUNYA_TOKEN,
    }

    # Utilisation de l'URL dynamique définie dans settings.py
    res = requests.post(settings.PAYDUNYA_BASE_URL, json=payload, headers=headers)
    data = res.json()

    if data.get("response_code") == "00":
        Payment.objects.create(
            user=user,
            amount=amount,
            plan_type=plan_type,
            token=data["token"],
            status="pending"
        )
        return Response({"payment_url": data["response_text"]})
    
    return Response(data, status=400)
    


@api_view(["GET"])
@permission_classes([AllowAny]) # PayDunya doit pouvoir y accéder sans être connecté
def payment_callback(request):
    # 1. Récupérer le token envoyé par PayDunya dans l'URL
    token = request.query_params.get("token")
    
    if not token:
        return Response({"error": "Token manquant"}, status=400)

    # 2. Vérifier si ce paiement existe dans notre base
    try:
        payment = Payment.objects.get(token=token)
        
        # Sécurité : On contacte PayDunya pour vérifier le statut réel du token
        # (Optionnel mais recommandé pour éviter la triche)
        verify_url = f"https://app.paydunya.com/api/v1/checkout-invoice/confirm/{token}"
        headers = {
            "PAYDUNYA-MASTER-KEY": settings.PAYDUNYA_MASTER_KEY,
            "PAYDUNYA-PRIVATE-KEY": settings.PAYDUNYA_PRIVATE_KEY,
            "PAYDUNYA-TOKEN": settings.PAYDUNYA_TOKEN,
        }
        verify_res = requests.get(verify_url, headers=headers)
        verify_data = verify_res.json()

        if verify_data.get("status") == "completed":
            # 3. Mettre à jour le paiement
            payment.status = "success"
            payment.save()

            # 4. Activer l'abonnement du User
            user = payment.user
            
            # Calcul de la durée
            if payment.plan_type == "monthly":
                duree = timedelta(days=30)
            else:
                duree = timedelta(days=365)

            # Mise à jour du profil utilisateur
            # (Assume que tu as ces champs dans ton User ou Profile)
            user.is_premium = True
            user.premium_until = timezone.now() + duree
            user.save()

            return Response({"status": "Paiement validé, accès accordé"})
        else:
            payment.status = "failed"
            payment.save()
            return Response({"status": "Échec du paiement chez PayDunya"})

    except Payment.DoesNotExist:
        return Response({"error": "Paiement introuvable"}, status=404)