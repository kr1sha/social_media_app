from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    id_user = models.IntegerField(verbose_name='id пользователя')
    bio = models.TextField(blank=True, verbose_name='описание пользователя')
    profile_image = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png', verbose_name='аватар пользователя')
    location = models.CharField(max_length=100, blank=True, verbose_name='адрес пользователя')

    def __str__(self):
        return self.user.username

