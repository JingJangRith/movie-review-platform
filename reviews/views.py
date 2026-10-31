from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from movies.models import Movie

from .forms import ReviewForm
from .models import Review


@login_required
def review_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)

    # Prevent one user from creating multiple reviews for the same movie.
    existing_review = Review.objects.filter(
        user=request.user,
        movie=movie,
    ).first()

    if existing_review:
        messages.error(
            request,
            "You have already reviewed this movie.",
        )
        return redirect("movie_detail", pk=movie.pk)

    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()

            messages.success(
                request,
                "Your review has been added successfully.",
            )
            return redirect("movie_detail", pk=movie.pk)
    else:
        form = ReviewForm()

    return render(
        request,
        "reviews/review_form.html",
        {
            "form": form,
            "movie": movie,
            "page_title": "Add Review",
        },
    )


@login_required
def review_edit(request, pk):
    review = get_object_or_404(
        Review,
        pk=pk,
        user=request.user,
    )

    if request.method == "POST":
        form = ReviewForm(
            request.POST,
            instance=review,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Your review has been updated successfully.",
            )
            return redirect(
                "movie_detail",
                pk=review.movie.pk,
            )
    else:
        form = ReviewForm(instance=review)

    return render(
        request,
        "reviews/review_form.html",
        {
            "form": form,
            "movie": review.movie,
            "page_title": "Edit Review",
        },
    )


@login_required
def review_delete(request, pk):
    review = get_object_or_404(
        Review,
        pk=pk,
        user=request.user,
    )

    if request.method == "POST":
        movie_pk = review.movie.pk
        review.delete()

        messages.success(
            request,
            "Your review has been deleted successfully.",
        )
        return redirect(
            "movie_detail",
            pk=movie_pk,
        )

    return render(
        request,
        "reviews/review_confirm_delete.html",
        {
            "review": review,
        },
    )