from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('settings', views.settings, name='settings'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    path('upload', views.upload, name='upload'),
    path('like_post/<int:post_id>', views.like_post, name='like_post'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search')
]
