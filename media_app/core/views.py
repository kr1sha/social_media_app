from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User

from .modules import get_image
from .models import Profile, Post, PostLike


@login_required(login_url='signin')
def settings(request):

    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        image = get_image(request, profile)
        bio = request.POST['bio']
        location = request.POST['location']

        profile.update_info(image, bio, location)
        profile.save()

        return redirect('settings')

    return render(request, 'setting.html', {'user_profile': profile})


@login_required(login_url='signin')
def index(request):

    profile = Profile.objects.get(user=request.user)
    posts = Post.objects.all()

    return render(request, 'index.html', {'profile': profile, 'posts': posts})


def signup(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        try:
            profile = Profile.create(request, username, email, password, password2)
        except ValidationError as e:
            [messages.info(request, error) for error in e]
            return redirect('signup')

        profile.save()

        return redirect('settings')

    else:
        return render(request, 'signup.html')


def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'signin.html')


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':

        username = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        post = Post.objects.create(username=username, image=image, caption=caption)
        post.save()

        return redirect('/')

    else:
        return redirect('/')


@login_required(login_url='signin')
def like_post(request, post_id):

    username = request.user.username
    post = Post.objects.get(id=post_id)
    existing_like = PostLike.objects.filter(post_id=post_id, username=username).first()

    if existing_like is None:

        new_like = PostLike.objects.create(post_id=post_id, username=username)
        new_like.save()

        post.increase_like()
        post.save()

        return redirect('/')

    else:
        existing_like.delete()
        post.decrease_like()
        post.save()
        return redirect('/')


@login_required(login_url='signin')
def profile(request, pk):

    user = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user)
    posts = Post.objects.filter(username=user.username)
    posts_count = len(posts)

    context = {'user': user, 'profile': user_profile, 'posts': posts, 'posts_count': posts_count}

    return render(request, 'profile.html', context)







