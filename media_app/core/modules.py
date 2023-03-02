from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def find_user_validation_errors(username: str, email: str, password: str, password2: str) -> list:
    """ Returns a list of errors that occur when trying to create a user with the current data """
    errors = []

    if password != password2:
        errors.append('Password not matching')

    if User.objects.filter(email=email).exists():
        errors.append('Email taken')

    if User.objects.filter(username=username).exists():
        errors.append('Username taken')

    return errors


def create_user(username: str, email: str, password: str, password2: str) -> User:
    """ Returning created user or raising validation error """
    errors = find_user_validation_errors(username, email, password, password2)
    if errors:
        raise ValidationError(errors)
    else:
        user = User.objects.create_user(username, email, password)
        user.save()
        return user


def get_image(request, profile):
    """ give image from request or give old profile image """
    image = request.FILES.get('image')
    if image is not None:
        return image
    else:
        return profile.profile_image

