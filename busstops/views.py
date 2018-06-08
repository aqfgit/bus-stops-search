from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from utils import scraper

@login_required
def index_view(request):
    data = scraper.run()
    return render(request, 'busstops/bus-search.html', {'data': data})