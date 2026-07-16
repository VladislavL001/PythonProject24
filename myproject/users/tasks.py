from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from datetime import timedelta

from django.utils import timezone
from users.models import Subscription, User


@shared_task
def send_course_update(course_id):
    """
    Отправка письма всем подписчикам курса.
    """

    subscriptions = Subscription.objects.filter(course_id=course_id)

    emails = [
        subscription.user.email
        for subscription in subscriptions
        if subscription.user.email
    ]

    if emails:
        send_mail(
            subject="Курс был обновлен",
            message="Материалы курса были обновлены. Зайдите в личный кабинет и ознакомьтесь с изменениями.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=emails,
            fail_silently=False,
        )


@shared_task
def deactivate_inactive_users():
    """
    Блокирует пользователей,
    которые не заходили более 30 дней.
    """

    month_ago = timezone.now() - timedelta(days=30)

    users = User.objects.filter(
        last_login__lt=month_ago,
        is_active=True,
    )

    count = users.update(is_active=False)

    return f"Заблокировано пользователей: {count}"