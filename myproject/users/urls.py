from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PaymentListAPIView, UserViewSet, RegisterAPIView, SubscriptionAPIView, PaymentCreateAPIView

router = DefaultRouter()

router.register(r"", UserViewSet, basename="User")

urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("subscription/", SubscriptionAPIView.as_view(), name="subscription"),

    path("", include(router.urls)),

    path("payment/create/", PaymentCreateAPIView.as_view(), name="payment-create"),
]
