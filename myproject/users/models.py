from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=35, blank=True, null=True)

    city = models.CharField(max_length=100, blank=True, null=True)

    avatar = models.ImageField(upload_to="users/", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    payment_date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True, related_name="payments")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=True, null=True, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    CASH = "cash"
    TRANSFER = "transfer"

    PAYMENT_METHODS = [
        (CASH, "Наличные"),
        (TRANSFER, "Перевод на счет"),
    ]

    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
