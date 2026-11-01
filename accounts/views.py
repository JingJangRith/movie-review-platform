from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.db.models import Avg

from .forms import RegisterForm, ProfileForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account has been created successfully.")
            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "You have logged out successfully.")

    return redirect("login")


@login_required
def profile_view(request):
    user_reviews = request.user.reviews.select_related("movie")

    review_count = user_reviews.count()
    average_rating = user_reviews.aggregate(
        average=Avg("rating")
    )["average"]

    recent_reviews = user_reviews[:5]

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)

    context = {
        "form": form,
        "review_count": review_count,
        "average_rating": average_rating,
        "recent_reviews": recent_reviews,
    }

    return render(request, "accounts/profile.html", context)

@login_required
def delete_account_view(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        logout(request)
        messages.success(request, "Your account has been deleted.")
        return redirect("login")

    return render(request, "accounts/delete_account.html")