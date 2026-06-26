from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (CourseViewSet, LessonListAPIView, LessonRetrieveAPIView, LessonCreateAPIView,
                    LessonUpdateAPIView, LessonDestroyAPIView)


router = DefaultRouter()

router.register(
    r'courses',
    CourseViewSet,
    basename='course'
)

urlpatterns = [
    path("", include(router.urls)),

    path(
        "lessons/",
        LessonListAPIView.as_view(),
        name="lesson_list"
    ),

    path(
        "lessons/<int:pk>/",
        LessonRetrieveAPIView.as_view(),
        name="lesson_detail"
    ),

    path(
        "lessons/create/",
        LessonCreateAPIView.as_view(),
        name="lesson_create"
    ),

    path(
        "lessons/update/<int:pk>/",
        LessonUpdateAPIView.as_view(),
        name="lesson_update"
    ),

    path(
        "lessons/delete/<int:pk>/",
        LessonDestroyAPIView.as_view(),
        name="lesson_delete"
    ),
]