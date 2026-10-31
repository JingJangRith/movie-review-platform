from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard_view(request):
    reviews = request.user.reviews.select_related("movie").all()

    context = {
        "reviews": reviews,
    }

    return render(request, "dashboard/dashboard.html", context)