from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from movies.models import Movie
from .models import Review


User = get_user_model()


class ReviewManagementTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="TestPassword123!",
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            password="TestPassword123!",
        )

        self.movie = Movie.objects.create(
            title="Test Movie",
            description="A movie for testing.",
            release_year=2025,
            director="Test Director",
            genre="Drama",
        )

        self.review = Review.objects.create(
            user=self.user,
            movie=self.movie,
            rating=80,
            comment="Great movie!",
        )

    def test_authenticated_user_can_create_review(self):
        movie = Movie.objects.create(
            title="Another Movie",
            description="Another movie for testing.",
            release_year=2024,
            director="Another Director",
            genre="Action",
        )

        self.client.login(
            username="testuser",
            password="TestPassword123!",
        )

        response = self.client.post(
            reverse("review_create", args=[movie.pk]),
            {
                "rating": 90,
                "comment": "Excellent movie!",
            },
        )

        self.assertEqual(Review.objects.filter(movie=movie).count(), 1)

        review = Review.objects.get(movie=movie)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.rating, 90)

    def test_unauthenticated_user_cannot_create_review(self):
        response = self.client.get(
            reverse("review_create", args=[self.movie.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_user_cannot_create_duplicate_review(self):
        self.client.login(
            username="testuser",
            password="TestPassword123!",
        )

        self.client.post(
            reverse("review_create", args=[self.movie.pk]),
            {
                "rating": 90,
                "comment": "Another review.",
            },
        )

        self.assertEqual(
            Review.objects.filter(
                user=self.user,
                movie=self.movie,
            ).count(),
            1,
        )

    def test_user_can_edit_own_review(self):
        self.client.login(
            username="testuser",
            password="TestPassword123!",
        )

        response = self.client.post(
            reverse("review_edit", args=[self.review.pk]),
            {
                "rating": 95,
                "comment": "Updated review!",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.review.refresh_from_db()

        self.assertEqual(self.review.rating, 95)
        self.assertEqual(
            self.review.comment,
            "Updated review!",
        )

    def test_user_cannot_edit_another_users_review(self):
        self.client.login(
            username="otheruser",
            password="TestPassword123!",
        )

        response = self.client.post(
            reverse("review_edit", args=[self.review.pk]),
            {
                "rating": 10,
                "comment": "Trying to edit.",
            },
        )

        self.assertEqual(response.status_code, 404)

        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, 80)

    def test_user_can_delete_own_review(self):
        self.client.login(
            username="testuser",
            password="TestPassword123!",
        )

        response = self.client.post(
            reverse("review_delete", args=[self.review.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Review.objects.filter(pk=self.review.pk).exists()
        )

    def test_user_cannot_delete_another_users_review(self):
        self.client.login(
            username="otheruser",
            password="TestPassword123!",
        )

        response = self.client.post(
            reverse("review_delete", args=[self.review.pk])
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            Review.objects.filter(pk=self.review.pk).exists()
        )