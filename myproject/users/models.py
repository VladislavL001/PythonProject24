from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from lms.models import Course, Lesson


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=35, blank=True, null=True)

    city = models.CharField(max_length=100, blank=True, null=True)

    avatar = models.ImageField(upload_to="users/", blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    payment_date = models.DateField()
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, blank=True, null=True, related_name="payments"
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, blank=True, null=True, related_name="payments"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    CASH = "cash"
    TRANSFER = "transfer"

    PAYMENT_METHODS = [
        (CASH, "Наличные"),
        (TRANSFER, "Перевод на счет"),
    ]

    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)

    payment_link = models.URLField(
        blank=True,
        null=True,
        max_length=1000,
    )


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )

    def __str__(self):
        return f"{self.user} -> {self.course}"
