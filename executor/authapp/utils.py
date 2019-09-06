from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from authapp.models import PyWebUser


def send_user_email(request, user, action=None):
    subject = message = None
    uid, token = TokenGenerator().generate_token(user)

    if action == "validate-email":
        subject = f"Please activate your account on {request.get_host()}"
        url = request.build_absolute_uri(
            reverse("validate-email", kwargs={"uid": uid, "token": token})
        )
        message = f"Follow the link below to complete the verification:\n{url}"

    elif action == "reset-password":
        subject = f"Reset password link on {request.get_host()}"
        url = request.build_absolute_uri(
            reverse("reset-password", kwargs={"uid": uid, "token": token})
        )
        message = f"Follow the link below to reset your password:\n{url}"

    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.is_active)

    def generate_token(self, user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = self.make_token(user)
        return uid, token

    def is_token_valid(self, uid, token):
        uid = force_text(urlsafe_base64_decode(uid))
        user = PyWebUser.objects.filter(pk=uid).first()
        return self.check_token(user, token), user
