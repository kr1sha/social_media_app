import random

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User

from .modules import get_image
from .models import Profile, Post, PostLike, Follow


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
    user_name = request.user.username
    user_follows = Follow.objects.filter(follower=user_name)
    user_followed_usernames = [user_follow.user for user_follow in user_follows]

    posts = Post.objects.filter(username__in=user_followed_usernames)
    profile = Profile.objects.get(user=request.user)
    suggestion_profiles = Profile.get_not_followed_by_user_profiles(user_followed_usernames, user_name)[:5]

    return render(request, 'index.html', {'profile': profile, 'posts': posts, 'suggestion_profiles': suggestion_profiles})


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

        return redirect('/')

    else:
        return redirect('/')


@login_required(login_url='signin')
def like_post(request, post_id):

    username = request.user.username
    post = Post.objects.get(id=post_id)
    existing_like = PostLike.objects.filter(post_id=post_id, username=username).first()

    if existing_like is None:
        new_like = PostLike.create_like(post, username)
        return redirect('/')

    else:
        existing_like.delete_like(post)
        return redirect('/')


@login_required(login_url='signin')
def profile(request, username):

    user_object = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user_object)
    posts = Post.objects.filter(username=user_object.username)
    posts_count = posts.count()
    follower_name = request.user.username

    follower_action = Follow.get_follower_action_name(username, follower_name)
    user_followers_count = Follow.objects.filter(user=username).count()
    user_following_count = Follow.objects.filter(follower=username).count()

    context = {'user_object': user_object,
               'profile': user_profile,
               'posts': posts,
               'posts_count': posts_count,
               'follower_action': follower_action,
               'user_followers_count': user_followers_count,
               'user_following_count': user_following_count}

    return render(request, 'profile.html', context)


@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':

        follower = request.POST['follower']
        user = request.POST['user']
        follow_object = Follow.objects.filter(follower=follower, user=user).first()

        if follow_object:
            follow_object.delete()
        else:
            new_follow = Follow.objects.create(follower=follower, user=user)

        return redirect('/profile/' + user)

    else:
        return redirect('/')


def search(request):
    username = request.user.username
    user_object = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        searched_username = request.POST['username']
        fonded_users = User.objects.filter(username__icontains=searched_username)
        founded_user_profiles = Profile.objects.filter(user__in=fonded_users)

        return render(request, 'search.html', {'user_profile': user_profile, 'founded_user_profiles': founded_user_profiles})

    return render(request, 'search.html', {'user_profile': user_profile})




