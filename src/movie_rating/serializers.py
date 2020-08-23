from rest_framework import serializers
from .models import MovieDetail, UserRating

class MovieDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieDetail
        lookup_field = 'id'
        fields = [
            'id', 'name', 'year', 'movie_rating', 'watch_list'
        ]


class UserRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRating
        lookup_field = 'id'
        fields = [
            'user',
            'movie',
            'rating',
            'user_watch_list',
        ]