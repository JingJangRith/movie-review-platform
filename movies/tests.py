from django.test import TestCase
from django.urls import reverse

from .models import Movie

from reviews.models import Review
from django.contrib.auth import get_user_model

User = get_user_model()


class MovieListTests(TestCase):

    def setUp(self):
        self.movie1 = Movie.objects.create(
            title="Inception",
            description="A science fiction movie.",
            release_year=2010,
            director="Christopher Nolan",
            genre="Sci-Fi",
        )

        self.movie2 = Movie.objects.create(
            title="The Dark Knight",
            description="A superhero movie.",
            release_year=2008,
            director="Christopher Nolan",
            genre="Action",
        )

        self.movie3 = Movie.objects.create(
            title="Interstellar",
            description="A space exploration movie.",
            release_year=2014,
            director="Christopher Nolan",
            genre="Sci-Fi",
        )

    def create_additional_movies(self):
        for number in range(4, 10):
            Movie.objects.create(
                title=f"Test Movie {number}",
                description="A movie for pagination testing.",
                release_year=2000 + number,
                director="Test Director",
                genre="Drama",
            )
    
    def test_movie_list_displays_six_movies_per_page(self):
        self.create_additional_movies()

        response = self.client.get(reverse("movie_list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["movies"]), 6)
        self.assertEqual(response.context["movies"].paginator.count, 9)
        self.assertTrue(response.context["movies"].has_next())

    def test_movie_list_second_page_displays_remaining_movies(self):
        self.create_additional_movies()

        response = self.client.get(
            reverse("movie_list"),
            {"page": 2},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["movies"]), 3)
        self.assertFalse(response.context["movies"].has_next())
        self.assertTrue(response.context["movies"].has_previous())

    def test_search_is_preserved_across_pages(self):
        self.create_additional_movies()

        Movie.objects.create(
            title="Another Nolan Movie",
            description="A test movie.",
            release_year=2020,
            director="Christopher Nolan",
            genre="Drama",
        )

        for number in range(2, 5):
            Movie.objects.create(
                title=f"Nolan Test Movie {number}",
                description="A test movie.",
                release_year=2020 + number,
                director="Christopher Nolan",
                genre="Drama",
            )

        response = self.client.get(
            reverse("movie_list"),
            {"q": "Christopher Nolan", "page": 2},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["query"], "Christopher Nolan")
        self.assertEqual(len(response.context["movies"]), 1)
        self.assertEqual(
            response.context["movies"][0].title,
            "The Dark Knight",
        )

    def test_genre_filter_is_preserved_across_pages(self):
        self.create_additional_movies()

        for number in range(6):
            Movie.objects.create(
                title=f"Action Movie {number}",
                description="An action movie.",
                release_year=2010 + number,
                director="Action Director",
                genre="Action",
            )

        response = self.client.get(
            reverse("movie_list"),
            {"genre": "Action", "page": 2},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["selected_genre"],
            "Action",
        )
        self.assertEqual(len(response.context["movies"]), 1)
        self.assertEqual(
            response.context["movies"][0].genre,
            "Action",
        )

    def test_year_filter_is_preserved_across_pages(self):
        self.create_additional_movies()

        for number in range(7):
            Movie.objects.create(
                title=f"Year Test Movie {number}",
                description="A movie for year filtering.",
                release_year=2020,
                director="Test Director",
                genre="Drama",
            )

        response = self.client.get(
            reverse("movie_list"),
            {"year": "2020", "page": 2},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["selected_year"], "2020")
        self.assertEqual(len(response.context["movies"]), 1)
        self.assertEqual(
            response.context["movies"][0].release_year,
            2020,
        )

    def test_sorting_is_preserved_across_pages(self):
        self.create_additional_movies()

        response = self.client.get(
            reverse("movie_list"),
            {"sort": "newest", "page": 2},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["selected_sort"], "newest")

        movies = list(response.context["movies"])

        years = [movie.release_year for movie in movies]

        self.assertEqual(years, sorted(years, reverse=True))

    def test_invalid_page_number_returns_first_page(self):
        self.create_additional_movies()

        response = self.client.get(
            reverse("movie_list"),
            {"page": "invalid"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["movies"].number, 1)

    def test_out_of_range_page_returns_last_page(self):
        self.create_additional_movies()

        response = self.client.get(
            reverse("movie_list"),
            {"page": 999},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["movies"].number, 2)

    def test_movie_list_page(self):
        response = self.client.get(reverse("movie_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Inception")
        self.assertContains(response, "The Dark Knight")
        self.assertContains(response, "Interstellar")

    def test_search_by_title(self):
        response = self.client.get(
            reverse("movie_list"),
            {"q": "Inception"},
        )

        self.assertContains(response, "Inception")
        self.assertNotContains(response, "The Dark Knight")

    def test_search_by_director(self):
        response = self.client.get(
            reverse("movie_list"),
            {"q": "Christopher Nolan"},
        )

        self.assertEqual(len(response.context["movies"]), 3)

    def test_search_by_genre(self):
        response = self.client.get(
            reverse("movie_list"),
            {"q": "Sci-Fi"},
        )

        self.assertEqual(len(response.context["movies"]), 2)

    def test_filter_by_genre(self):
        response = self.client.get(
            reverse("movie_list"),
            {"genre": "Action"},
        )

        self.assertEqual(len(response.context["movies"]), 1)
        self.assertEqual(
            response.context["movies"][0],
            self.movie2,
        )

    def test_filter_by_year(self):
        response = self.client.get(
            reverse("movie_list"),
            {"year": "2010"},
        )

        self.assertEqual(len(response.context["movies"]), 1)
        self.assertEqual(
            response.context["movies"][0],
            self.movie1,
        )

    def test_combined_search_and_filters(self):
        response = self.client.get(
            reverse("movie_list"),
            {
                "q": "Christopher Nolan",
                "genre": "Sci-Fi",
                "year": "2014",
            },
        )

        self.assertEqual(len(response.context["movies"]), 1)
        self.assertEqual(
            response.context["movies"][0],
            self.movie3,
        )

    def test_invalid_year_returns_no_results(self):
        response = self.client.get(
            reverse("movie_list"),
            {"year": "invalid"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["movies"]), 0)

    def test_default_sorting_by_title(self):
        response = self.client.get(reverse("movie_list"))

        movies = list(response.context["movies"])

        self.assertEqual(
            [movie.title for movie in movies],
            ["Inception", "Interstellar", "The Dark Knight"],
        )

    def test_sort_newest_first(self):
        response = self.client.get(
            reverse("movie_list"),
            {"sort": "newest"},
        )

        movies = list(response.context["movies"])

        self.assertEqual(
            [movie.release_year for movie in movies],
            [2014, 2010, 2008],
        )

    def test_sort_oldest_first(self):
        response = self.client.get(
            reverse("movie_list"),
            {"sort": "oldest"},
        )

        movies = list(response.context["movies"])

        self.assertEqual(
            [movie.release_year for movie in movies],
            [2008, 2010, 2014],
        )

    def test_invalid_sort_falls_back_to_title(self):
        response = self.client.get(
            reverse("movie_list"),
            {"sort": "invalid"},
        )

        movies = list(response.context["movies"])

        self.assertEqual(
            [movie.title for movie in movies],
            ["Inception", "Interstellar", "The Dark Knight"],
        )

    def test_movie_detail_page(self):
        response = self.client.get(
            reverse("movie_detail", args=[self.movie1.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Inception")
        self.assertContains(response, "Christopher Nolan")

    def test_nonexistent_movie_returns_404(self):
        response = self.client.get(
            reverse("movie_detail", args=[9999])
        )

        self.assertEqual(response.status_code, 404)

class MovieTemperatureTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="TestPassword123!",
        )

        self.movie = Movie.objects.create(
            title="Temperature Test Movie",
            description="Testing temperature ratings.",
            release_year=2025,
            director="Test Director",
            genre="Drama",
        )

    def create_review(self, rating, username):
        user = User.objects.create_user(
            username=username,
            password="TestPassword123!",
        )

        Review.objects.create(
            user=user,
            movie=self.movie,
            rating=rating,
            comment="This is a test review.",
        )

    def test_movie_without_reviews(self):
        response = self.client.get(
            reverse("movie_detail", args=[self.movie.pk])
        )

        self.assertIsNone(response.context["average_temperature"])
        self.assertEqual(
            response.context["temperature_category"],
            "Not rated yet",
        )

    def test_average_temperature(self):
        self.create_review(60, "user1")
        self.create_review(80, "user2")

        response = self.client.get(
            reverse("movie_detail", args=[self.movie.pk])
        )

        self.assertEqual(response.context["average_temperature"], 70)
        self.assertEqual(
            response.context["temperature_category"],
            "Hot",
        )

    def test_temperature_categories(self):
        test_cases = [
            (19, "Freezing"),
            (20, "Cold"),
            (39, "Cold"),
            (40, "Warm"),
            (59, "Warm"),
            (60, "Hot"),
            (79, "Hot"),
            (80, "Blazing"),
            (100, "Blazing"),
        ]

        for rating, expected_category in test_cases:
            with self.subTest(rating=rating):
                self.movie.reviews.all().delete()
                self.create_review(rating, f"user{rating}")

                response = self.client.get(
                    reverse("movie_detail", args=[self.movie.pk])
                )

                self.assertEqual(
                    response.context["temperature_category"],
                    expected_category,
                )

    def test_average_uses_half_up_rounding(self):
        self.create_review(79, "user1")
        self.create_review(80, "user2")

        response = self.client.get(
            reverse("movie_detail", args=[self.movie.pk])
        )

        self.assertEqual(response.context["average_temperature"], 80)
        self.assertEqual(
            response.context["temperature_category"],
            "Blazing",
        )