from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import User, Payment, Subscription
from .serializers import UserSerializer, PaymentSerializer, RegisterSerializer
from lms.models import Course
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiExample
from .services import (
    create_product,
    create_price,
    create_session,
)


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]

    permission_classes = [IsAuthenticated]

    filterset_fields = [
        "course",
        "lesson",
        "payment_method",
    ]

    ordering_fields = [
        "payment_date",
    ]

@extend_schema(tags=["Users"],)
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

@extend_schema(tags=["Payments"],)
class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

@extend_schema(
    tags=["Subscriptions"],
    summary="Подписка на курс",
    description="Добавляет или удаляет подписку пользователя на курс."
)
class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Подписаться или отписаться от курса",
        description="Если подписка существует — удаляет её, иначе создает.",
        examples=[
            OpenApiExample(
                "Пример запроса",
                value={
                    "course_id": 1,
                },
                request_only=True,
            ),
        ],
    )
    def post(self, request):
        user = request.user

        course_id = request.data.get("course_id")

        course = get_object_or_404(
            Course,
            pk=course_id,
        )

        subscription = Subscription.objects.filter(
            user=user,
            course=course,
        )

        if subscription.exists():
            subscription.delete()
            message = "Подписка удалена"

        else:
            Subscription.objects.create(
                user=user,
                course=course,
            )
            message = "Подписка добавлена"

        return Response(
            {
                "message": message
            }
        )

class PaymentCreateAPIView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):

        payment = serializer.save(
            user=self.request.user
        )

        product = create_product(payment)

        price = create_price(
            payment,
            product,
        )

        session = create_session(price)

        payment.payment_link = session.url
        payment.save()