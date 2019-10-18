from django.urls import path

from . import handler

urlpatterns = [
    path('search', handler.search),
    path('changePasswd', handler.change_passwd),
    path('setPasswd', handler.set_passwd),
    path('uploadArticle', handler.upload_article)
]