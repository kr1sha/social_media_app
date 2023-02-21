from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

from .modules import create_user
from .models import Profile


def index(request):
    return render(request, 'index.html')


def signup(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        try:
            user = create_user(username, email, password, password2)
        except ValidationError as e:
            [messages.info(request, error) for error in e]
            return redirect('signup')

        profile = Profile.objects.create(user=user, id_user=user.id)
        profile.save()

        redirect('login')

    else:
        return render(request, 'signup.html')
