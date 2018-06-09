from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from utils import scraper
import json


@login_required
def index_view(request):
    if request.method == 'POST':
        data = request.body
        print(data)
        results = scraper.run(data)
        return HttpResponse(results)
    else:
        return render(request, 'busstops/bus-search.html')
