# HOME PAGE URLS
from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$',  views.home, name='homeP'),
    url(r'^result',  views.result, name='resP',),
]
