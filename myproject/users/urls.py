from django.urls import path

from .views import UserUpdateAPIView, PaymentListAPIView

urlpatterns = [
    path("users/update/<int:pk>/", UserUpdateAPIView.as_view(), name="user_update"),
    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),
]
