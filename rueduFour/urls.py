from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('comptabilite.urls')),
    path('admin/', admin.site.urls, name='admin'),
]
