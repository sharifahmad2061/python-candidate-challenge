from django.urls import path
from . import views

urlpatterns = [
    path('<lat>/<long>/<page>', views.index, name='home'),
    path('photos/<int:page>', views.photos, name='next_page')
]
