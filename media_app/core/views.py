from django.http import HttpResponse


def index(request):
    return HttpResponse("<h1>It's fine. Probably</h1>")