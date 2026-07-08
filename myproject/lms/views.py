from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsModerator, IsOwner
from .models import Course, Lesson
from .paginators import LessonAndCoursePagination
from .serializers import CourseSerializer, LessonSerializer
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Courses"],)
class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = LessonAndCoursePagination

    def get_queryset(self):
        if self.request.user.groups.filter(name="Moderators").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):

        if self.action == "create":
            permission_classes = [
                IsAuthenticated,
                ~IsModerator,
            ]

        elif self.action == "destroy":
            permission_classes = [
                IsAuthenticated,
                IsOwner,
            ]

        elif self.action in [
            "retrieve",
            "update",
            "partial_update",
        ]:
            permission_classes = [
                IsAuthenticated,
                IsModerator | IsOwner,
            ]

        else:
            permission_classes = [
                IsAuthenticated,
            ]

        return [permission() for permission in permission_classes]

@extend_schema(tags=["Lessons"],)
class LessonListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    pagination_class = LessonAndCoursePagination

    def get_queryset(self):
        if self.request.user.groups.filter(name="Moderators").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):

        if self.request.method == "POST":
            permission_classes = [
                IsAuthenticated,
                ~IsModerator,
            ]
        else:
            permission_classes = [
                IsAuthenticated,
            ]

        return [permission() for permission in permission_classes]


@extend_schema(tags=["Lessons"],)
class LessonRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = LessonSerializer

    def get_queryset(self):
        if self.request.user.groups.filter(name="Moderators").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)

    def get_permissions(self):

        if self.request.method == "DELETE":
            permission_classes = [
                IsAuthenticated,
                IsOwner,
            ]

        else:
            permission_classes = [
                IsAuthenticated,
                IsModerator | IsOwner,
            ]

        return [permission() for permission in permission_classes]



