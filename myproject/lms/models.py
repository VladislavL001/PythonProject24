from django.conf import settings
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=200)

    preview = models.ImageField(upload_to="courses/", blank=True, null=True)

    description = models.TextField(blank=True, null=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="courses",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")

    name = models.CharField(max_length=200)

    description = models.TextField(blank=True, null=True)

    preview = models.ImageField(upload_to="lessons/", blank=True, null=True)

    video_url = models.URLField(blank=True, null=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="lessons",
    )

    def __str__(self):
        return self.name
