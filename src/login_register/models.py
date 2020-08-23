from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist

class Profile(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')    
    email_confirmed = models.BooleanField(default=False)
    token           = models.CharField(max_length=200, blank=True, null=True)
    is_active       = models.BooleanField(default=False, null=True)
        
    
    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)