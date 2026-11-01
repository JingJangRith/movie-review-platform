from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.shortcuts import render


@login_required
def dashboard_view(request):
    reviews = request.user.reviews.select_related("movie").all()

    statistics = request.user.reviews.aggregate(
        total_reviews=Count("id"),
        average_temperature=Avg("rating"),
    )

    context = {
        "reviews": reviews,
        "total_reviews": statistics["total_reviews"],
        "average_temperature": statistics["average_temperature"],
    }

    return render(request, "dashboard/dashboard.html", context)