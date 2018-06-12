from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.
def index_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('busstops:index'))

    return render(request, 'registration/login.html')


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('busstops:index'))

    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        return HttpResponseRedirect(reverse('registration:index'))

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('busstops:index'))
    else:
        return HttpResponseRedirect(reverse('registration:index'))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('registration:index'))
