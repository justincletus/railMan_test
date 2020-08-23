from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from django.urls import re_path, reverse
from django.contrib.auth import get_user_model
#from allauth.account.views import ConfirmEmailView
from django.views.generic.base import TemplateView, TemplateResponseMixin, View
from railMan_test import app_settings
from railMan_test import settings
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from .token import account_activation_token
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import HttpResponse, Http404, JsonResponse
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from .forms import SignupForm
from django.urls import get_resolver
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import response, decorators, permissions, status
from .serializers import UserCreateSerializer


def home_view(request, *args, **kwargs):
    user = request.user
    
    return render(request, 'home.html')

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {
            'message': 'Hello World'
        }

        return Response(content)



User = get_user_model()
@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def signup(request, *args, **kwargs):

    serializer = UserCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    user = serializer.save()

    user.refresh_from_db()            
    user.profile.is_active = False
    token = account_activation_token.make_token(user)             
    user.profile.token = token
    user.is_active = False           
    user.profile.save()
    #print(urlsafe_base64_encode(force_bytes(user.pk)))
    
    current_site = get_current_site(request)
    mail_subject = 'Activate your account.'
    message = render_to_string('core/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token,
    })
    req_email = request.data['email']
    email = EmailMessage(
                mail_subject, message, to=[req_email]
    )
    email.content_subtype = "html"
    email.send()

    refresh = RefreshToken.for_user(user) 
    res = {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }

    return Response(res, status.HTTP_201_CREATED)

def save(request, form):
    username = email = form.cleaned_data.get('email')
    first_name= form.cleaned_data.get('first_name')
    last_name = form.cleaned_data.get('last_name')
    password = form.cleaned_data.get('password')
    return User.objects.create_user(username, email=email, password=password, first_name=first_name, last_name=last_name)

@login_required
def profile(request):
    current_user = request.user
    user = User.objects.get(pk=current_user.id)
    profile = Profile.objects.filter(user=user).get()    

    if not profile.email_confirmed:
        messages.success(request, f'Account is created for {profile.user}! to need to confirm your email before login')
        return redirect('login')
    
    context = {
        "profile": profile
    }
    return render(request, 'profile.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))

        user = User.objects.get(pk=uid)
        profile = Profile.objects.filter(user=user).get()
        
        if(user.profile.token == profile.token):
            profile.refresh_from_db()
            profile.is_active = True
            profile.email_confirmed = True
            profile.save()
            context = {
                "message": "Thank you for your email confirmation. Now you can login your account."
            }
            return render(request, 'core/send_email.html', context)
        else:
            context = {
                "message": "access denied."
            }
            return render(request, 'core/send_email.html', context)
        
    except(TypeError, ValueError, OverflowError):
        user = None
        return HttpResponse('Activation link is invalid!')


def createTokenUser(request, *args, **kwargs):
    user = request.user
    refresh = RefreshToken.for_user(user)

    data = {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }

    return JsonResponse(data)

@decorators.api_view(['GET'])
def jwt_response_payload_handler(request, token=None):
    user = request.user
    # print(user.username)
    return Response({
        'token': token,
        'username': user.username,
        'user_id': user.id,
        'email': user.email
    }) 
