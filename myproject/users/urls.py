from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PaymentListAPIView, UserViewSet, RegisterAPIView

router = DefaultRouter()

router.register(r"", UserViewSet, basename="User")

urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("", include(router.urls)),
]
