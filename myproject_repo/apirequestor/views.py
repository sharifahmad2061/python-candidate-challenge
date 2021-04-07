from django.shortcuts import render
from django.conf import settings

import requests

API_KEY = getattr(settings, 'FLICKR_API_KEY', None)
API_URL = ("https://api.flickr.com/services/rest/"
            "?method=flickr.places.findByLatLon"
            "&api_key={}&lat={}&lon={}&format=json")

# Create your views here.
def index(request):
    if request.method == 'GET':
        return render(request, 'apirequestor/index.html')
    elif request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        url = API_URL.format(API_KEY, latitude, longitude)
        print(url)
        response = requests.get(url)
        print(response)
        return render(requests, 'apirequestor/index.html')