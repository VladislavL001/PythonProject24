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

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

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