
from django.contrib import admin
from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_year", "director", "genre")
    search_fields = ("title", "director", "genre")
    list_filter = ("genre", "release_year")
    ordering = ("title",)