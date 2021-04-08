from django.shortcuts import render
from django.conf import settings
from .models import Location

import requests as req_mod

API_KEY = getattr(settings, 'FLICKR_API_KEY', None)

API_URL = ("https://api.flickr.com/services/rest/"
            "?method=flickr.photos.search"
            "&api_key={}&lat={}&lon={}&format=json&nojsoncallback=1&page={}&per_page=10")


def call_api(lat, lon, page=1):
    print(lat, lon, page)
    url = API_URL.format(API_KEY, lat, lon, page)
    response = req_mod.get(url).json()
    # print(response)
    context = {
        'to': {
            'photos': [],
            'pages': response.get('photos').get('pages'),
            'prev': response.get('photos').get('page') + 1 if response.get('photos').get('page') > 1 else None,
            'page': response.get('photos').get('page'),
            'lat': lat,
            'lon': lon
        }
    }
    for each_photo in response['photos']['photo']:
        el  = {}
        el['id'] = each_photo.get('id')
        el['secret'] = each_photo.get('secret')
        el['server'] = each_photo.get('server')
        el['name'] = each_photo.get('title')
        context.get('to').get('photos').append(el)
    return context

# Create your views here.
def index(request):
    if request.method == 'GET':
        context = {
            'to': {
                'photos': []
            }
        }
        for pic in Location.objects.all()[:10].values():
            el  = {}
            el['id'] = pic.get('image_id')
            el['secret'] = pic.get('secret')
            el['server'] = pic.get('server')
            el['name'] = pic.get('name')
            context.get('to').get('photos').append(el)
        # print(context)
        return render(request, 'apirequestor/index.html', context)

def photos(request):
    if request.method == 'GET':
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')
        page_number = 1 if not request.GET.get('page') else request.GET.get('page')
        context = call_api(lat=latitude, lon=longitude, page=page_number)

        # save to db
        locations = []
        for each_pic in context.get('to').get('photos'):
            locations.append(
                Location(name=each_pic.get('name'),
                         image_id=each_pic.get('id'),
                         server=each_pic.get('server'),
                         secret=each_pic.get('secret'),
                         latitude=latitude,
                         longitude=longitude))
        # print(locations)
        Location.objects.bulk_create(locations)


        return render(request, 'apirequestor/index.html', context)
