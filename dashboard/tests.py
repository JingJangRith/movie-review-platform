from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from movies.models import Movie
from reviews.models import Review

User = get_user_model()


class DashboardTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="TestPassword123!",
        )

        self.movie1 = Movie.objects.create(
            title="Inception",
            description="A science fiction movie.",
            release_year=2010,
            director="Christopher Nolan",
            genre="Sci-Fi",
        )

        self.movie2 = Movie.objects.create(
            title="Interstellar",
            description="A space exploration movie.",
            release_year=2014,
            director="Christopher Nolan",
            genre="Sci-Fi",
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_access_dashboard(self):
        self.client.login(
            username="testuser",
            password="TestPassword123!",
        )

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)

    def test_dashboard_displays_review_statistics(self):
        Review.objects.create(
            user=self.user,
            movie=self.movie1,
            rating=60,
            comment="Good movie.",
        )

        Review.objects.create(
            user=self.user,
            movie=self.movie2,
            rating=80,
            comment="Excellent movie.",
        )

        self.client.login(
            username="testuser",
            password="TestPassword123!",
        )

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.context["total_reviews"], 2)
        self.assertEqual(
            response.context["average_temperature"],
            70,
        )

    def test_dashboard_without_reviews(self):
        self.client.login(
            username="testuser",
            password="TestPassword123!",
        )

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.context["total_reviews"], 0)
        self.assertIsNone(
            response.context["average_temperature"],
        )
        self.assertContains(response, "You haven't written any reviews yet.")