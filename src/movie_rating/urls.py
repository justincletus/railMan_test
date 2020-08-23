from django.urls import path, re_path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('create/', views.createMovie, name="movies"),
    path('movie-list/', views.movieList, name="movie_list"),
    path('user-rating/', views.ratingByUser, name="rating_by_user"),
    path('watch_list/', views.watchListByUser, name="watch_list"),
    re_path(r'^movie-list/(?P<pk>\d+)/$', views.movieItem, name="movie_item"),
    re_path(r'^movie-list/(?P<pk>\d+)/user-rating/$', views.userRating, name="user_raing"),
]