# payments/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Payment(models.Model):
    STATUS_CHOICES = [
        ("pending", "En attente"),
        ("success", "Réussi"),
        ("failed", "Échoué"),
    ]

    # Ajout du type de plan
    PLAN_CHOICES = [
        ("monthly", "Mensuel"),
        ("yearly", "Annuel"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    amount = models.PositiveIntegerField()
    plan_type = models.CharField(max_length=10, choices=PLAN_CHOICES, default="monthly") # Nouveau
    token = models.CharField(max_length=255, unique=True, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan_type} - {self.status}"
