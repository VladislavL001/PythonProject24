from rest_framework import serializers
from users.models import Subscription

from .models import Course, Lesson
from .validators import YouTubeValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"

        validators = [YouTubeValidator(field="video_url")]


class CourseSerializer(serializers.ModelSerializer):

    lessons_count = serializers.SerializerMethodField()

    lessons = LessonSerializer(
        many=True,
        read_only=True,
    )

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "preview",
            "description",
            "lessons_count",
            "lessons",
            "is_subscribed",
        ]

    @staticmethod
    def get_lessons_count(obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get("request")

        if request is None or request.user.is_anonymous:
            return False

        return Subscription.objects.filter(
            user=request.user,
            course=obj,
        ).exists()
