from django.urls import path

from . import handler

urlpatterns = [
    path('', handler.search),
]