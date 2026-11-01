from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Q, Avg
from django.shortcuts import get_object_or_404, render

from .models import Movie


def movie_list(request):
    movies = Movie.objects.all()

    query = request.GET.get("q", "").strip()
    genre = request.GET.get("genre", "").strip()
    year = request.GET.get("year", "").strip()
    sort = request.GET.get("sort", "title").strip()

    # Search by title, director, or genre.
    if query:
        movies = movies.filter(
            Q(title__icontains=query)
            | Q(director__icontains=query)
            | Q(genre__icontains=query)
        )

    sort_options = {
    "title": "title",
    "newest": "-release_year",
    "oldest": "release_year",
}
    movies = movies.order_by(
        sort_options.get(sort, "title")
    )

    # Filter by genre.
    if genre:
        movies = movies.filter(genre__iexact=genre)

    # Filter by release year.
    if year:
        if year.isdigit():
            movies = movies.filter(release_year=int(year))
        else:
            movies = movies.none()

    genres = (
        Movie.objects
        .values_list("genre", flat=True)
        .distinct()
        .order_by("genre")
    )

    context = {
        "movies": movies,
        "query": query,
        "selected_genre": genre,
        "selected_year": year,
        "genres": genres,
    }

    return render(request, "movies/movie_list.html", context)


def movie_detail(request, pk):
    movie = get_object_or_404(
        Movie.objects.prefetch_related("reviews__user"),
        pk=pk,
    )

    reviews = movie.reviews.all()
    average = reviews.aggregate(value=Avg("rating"))["value"]

    user_reviewed = False

    if request.user.is_authenticated:
        user_reviewed = reviews.filter(user=request.user).exists()

    if average is not None:
        average = int(
            Decimal(str(average)).quantize(
                Decimal("1"),
                rounding=ROUND_HALF_UP,
            )
        )

        if average <= 19:
            temperature_category = "Freezing"
        elif average <= 39:
            temperature_category = "Cold"
        elif average <= 59:
            temperature_category = "Warm"
        elif average <= 79:
            temperature_category = "Hot"
        else:
            temperature_category = "Blazing"
    else:
        temperature_category = "Not rated yet"

    return render(
        request,
        "movies/movie_detail.html",
        {
            "movie": movie,
            "reviews": reviews,
            "average_temperature": average,
            "temperature_category": temperature_category,
            "user_reviewed": user_reviewed,
        },
    )