from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
import re
from railMan_test.utils import removeHtmlTag
from bs4 import BeautifulSoup
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .web_scraping import WebScrap
from .models import MovieDetail, UserRating
from django.contrib import messages
from django.http import Http404
from rest_framework import viewsets, generics, status
from .serializers import MovieDetailSerializer, UserRatingSerializer
from django.contrib.auth.models import User

def createMovie(request, *args, **kwargs):

    web_scrap_client = WebScrap()
    movie_list = web_scrap_client.getHtmlContent()

    for movie in movie_list:
        item = MovieDetail()
        item.name = movie['name']
        item.slug = movie['slug']
        item.year = movie['year']
        item.movie_rating = movie['rating']
        item.save()
        print(item.id)    

    data = {
        'data': 'created movies'
    }

    return JsonResponse(data, safe=False)


# @api_view(['GET'])
def movieList(request, *args, **kwargs):
    movies = MovieDetail.objects.all()

    movies = list(movies.values())

    items = {
        'movies': movies
    }

    return JsonResponse(items, safe=False)


@api_view(['GET'])
def movieItem(request, pk, *args, **kwargs):

    try:
        movie = get_object_or_404(MovieDetail, id=pk)
        

    except MovieDetail.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = MovieDetailSerializer(movie)

    return Response(serializer.data)


@api_view(['POST'])
def userRating(request, pk, *args, **kwargs):

    try:
        movie = get_object_or_404(MovieDetail, id=pk)        
        user = request.user        
        serializer = UserRatingSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        rating = serializer.save()

    except MovieDetail.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = {
        'user-rating-saved': status.HTTP_201_CREATED
    }

    return Response(data)


@api_view(['GET'])
def ratingByUser(request, *args, **kwargs):
    user = request.user
    try:
        user = get_object_or_404(User, id=user.id)
        rating = UserRating.objects.all().filter(user=user.id)
        rating = list(rating.values())
    
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)    

    data = {
        'user-rating': rating
    }

    return JsonResponse(data, safe=False)


@api_view(['GET'])
def watchListByUser(request, *args, **kwargs):
    user = request.user
    try:
        user = get_object_or_404(User, id=user.id)
        watch_list = UserRating.objects.all().filter(user=user.id)
        watch_list = list(watch_list.values())
    
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = {
        'watch-list': watch_list
    }

    return JsonResponse(data, safe=False)




