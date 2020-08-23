from django.contrib import admin
from .models import MovieDetail, UserRating


class MovieDetailAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'year',
        'movie_rating'
    ]

admin.site.register(MovieDetail, MovieDetailAdmin)

class UserRatingAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'movie',
        'rating'
    ]

admin.site.register(UserRating, UserRatingAdmin)