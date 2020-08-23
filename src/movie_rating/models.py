from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify
from datetime import datetime

class MovieDetail(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    actor = models.CharField(max_length=50, blank=True, null=True)
    year = models.IntegerField(default=None)
    movie_rating = models.FloatField(default=None)
    watch_list = models.BooleanField(default=False)
    

    def __str__(self):
        return self.name

def pre_save_receiver(sender, instance, *args, **kwargs):
    slug = slugify(instance.name)
    exists = MovieDetail.objects.filter(slug=slug).exists()
    if exists:
        slug = "%s-%s" %(slug, instance.id)
    instance.slug = slug

pre_save.connect(pre_save_receiver, sender=MovieDetail)



class UserRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(MovieDetail, on_delete=models.CASCADE)
    rating = models.FloatField(default=None)
    user_watch_list = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


