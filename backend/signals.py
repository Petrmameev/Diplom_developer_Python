from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.dispatch import Signal, receiver
from django_rest_passwordreset.signals import reset_password_token_created

from backend.models import User

new_user_registered = Signal()

new_order = Signal()


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):
    """
    Отправляем письмо с токеном для сброса пароля
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param kwargs:
    :return:
    """
    # send an e-mail to the user

    msg = EmailMultiAlternatives(
        # title:
        f"Password Reset Token for {reset_password_token.user}",
        # message:
        reset_password_token.key,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email],
    )
    msg.send()


def new_user_registered_signal_mail(user):
    """
    отправляем письмо с подтрердждением почты
    """
    # send an e-mail to the user
    # token, _ = ConfirmEmailToken.objects.get_or_create(user=user)

    send_mail(
        # title:
        # f"Password Reset Token for {user.email}",
        f"You have been registered",
        # message:
        # token.key,
        f"You have been registered",
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [user.email],
        fail_silently=False,
    )


@receiver(new_order)
def new_order_signal(user_id, **kwargs):
    """
    отправяем письмо при изменении статуса заказа
    """
    # send an e-mail to the user
    user = User.objects.get(id=user_id)

    msg = EmailMultiAlternatives(
        # title:
        f"Обновление статуса заказа",
        # message:
        "Заказ сформирован",
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [user.email],
    )
    msg.send()
