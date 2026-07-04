from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from users.models import User, Subscription


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@test.ru",
            password="12345678"
        )

        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            name="Python",
            owner=self.user
        )

        self.lesson = Lesson.objects.create(
            course=self.course,
            name="Lesson 1",
            video_url="https://youtube.com/watch?v=test",
            owner=self.user
        )

    def test_lesson_list(self):
        response = self.client.get("/api/lessons/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_create(self):
        data = {
            "course": self.course.id,
            "name": "Lesson 2",
            "video_url": "https://youtube.com/watch?v=123"
        }

        response = self.client.post(
            "/api/lessons/",
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_lesson_retrieve(self):
        response = self.client.get(
            f"/api/lessons/{self.lesson.pk}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_update(self):
        response = self.client.patch(
            f"/api/lessons/{self.lesson.pk}/",
            {
                "name": "Updated lesson"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_delete(self):
        response = self.client.delete(
            f"/api/lessons/{self.lesson.pk}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="user2@test.ru",
            password="12345678"
        )

        self.client.force_authenticate(
            user=self.user
        )

        self.course = Course.objects.create(
            name="Python",
            owner=self.user
        )

    def test_subscription_create(self):
        response = self.client.post(
            "/users/subscription/",
            {
                "course_id": self.course.id
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertTrue(
            Subscription.objects.filter(
                user=self.user,
                course=self.course
            ).exists()
        )

    def test_subscription_delete(self):

        Subscription.objects.create(
            user=self.user,
            course=self.course
        )

        response = self.client.post(
            "/users/subscription/",
            {
                "course_id": self.course.id
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertFalse(
            Subscription.objects.filter(
                user=self.user,
                course=self.course
            ).exists()
        )