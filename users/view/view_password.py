from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

User = get_user_model()

class RequestPasswordResetView(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)

            reset_link = f"https://localhost:5173/reset-password/{uid}/{token}"

            context = {
                'user_first_name': user.first_name or '',
                'reset_link': reset_link,
                'app_name': "Learn Informatique"
            }

            email_html_message = render_to_string('emails/password_reset_email.html', context)
            email_text_message = render_to_string('emails/password_reset_email.txt', context)

            email_message = EmailMultiAlternatives(
                subject="Réinitialisation de votre mot de passe - InfoSits",
                body=email_text_message,  # texte brut obligatoire
                from_email=None,  # prendra DEFAULT_FROM_EMAIL
                to=[user.email]
            )
            email_message.attach_alternative(email_html_message, "text/html")
            email_message.send()

            return Response({"message": "Un email avec les instructions a été envoyé."})
        except User.DoesNotExist:
            return Response({"error": "Aucun compte associé à cet email."}, status=status.HTTP_404_NOT_FOUND)

class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"error": "Lien invalide ou expiré."}, status=status.HTTP_400_BAD_REQUEST)

            new_password = request.data.get("new_password")
            re_new_password = request.data.get("re_new_password")

            if new_password != re_new_password:
                return Response({"error": "Les mots de passe ne correspondent pas."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            return Response({"message": "Mot de passe réinitialisé avec succès."})
        except Exception as e:
            return Response({"error": "Erreur lors de la réinitialisation."}, status=status.HTTP_400_BAD_REQUEST)
