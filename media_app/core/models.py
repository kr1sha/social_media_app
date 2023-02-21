from django.contrib import auth
from django.contrib.auth.models import User
from django.db import models

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


