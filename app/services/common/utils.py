import random
from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken


def generate_otp(length=6):
    otp = ''.join([str(random.randint(0, 9)) for _ in range(length)])
    return otp


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def send_otp_mail(otp, receiver):
    email = EmailMessage(
        subject='otp for warehouse',
        body=f'{otp}',
        to=[receiver],
    )
    email.send()