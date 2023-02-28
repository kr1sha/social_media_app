from django.contrib import auth
from django.contrib.auth.models import User
from django.db import models
import uuid
from datetime import datetime

from .modules import create_user


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    id_user = models.IntegerField(verbose_name='id пользователя')
    bio = models.TextField(blank=True, verbose_name='описание пользователя')
    profile_image = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png', verbose_name='аватар пользователя')
    location = models.CharField(max_length=100, blank=True, verbose_name='адрес пользователя')

    def update_info(self, image, bio: str, location: str):
        self.profile_image = image
        self.bio = bio
        self.location = location

    def __str__(self):
        return self.user.username

    @classmethod
    def create(cls, request, username: str, email: str, password: str, password2: str):
        user = create_user(username, email, password, password2)

        user_login = auth.authenticate(username=username, password=password)
        auth.login(request, user_login)

        profile = cls(user=user, id_user=user.id)
        return profile


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name='id')
    username = models.CharField(max_length=100, verbose_name='Имя пользователя')
    image = models.ImageField(upload_to='post_image', verbose_name='Фото')
    caption = models.TextField(verbose_name='Подпись')
    created_at = models.DateTimeField(default=datetime.now, verbose_name='Дата создания')
    number_of_likes = models.IntegerField(default=0, verbose_name='Колличество лайков')

    def increase_like(self):
        self.number_of_likes += 1

    def decrease_like(self):
        self.number_of_likes -= 1

    def get_id(self):
        return int(self.id)

    def __str__(self):
        return self.username


class PostLike(models.Model):
    post_id = models.CharField(max_length=500, verbose_name='id поста')
    username = models.CharField(max_length=100, verbose_name='Имя пользователя')

    def __str__(self):
        return self.username
