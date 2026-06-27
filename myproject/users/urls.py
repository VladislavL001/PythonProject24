from django.urls import path

from .views import UserUpdateAPIView

urlpatterns = [
    path(
        "users/update/<int:pk>/",
        UserUpdateAPIView.as_view(),
        name="user_update",
    ),
]
