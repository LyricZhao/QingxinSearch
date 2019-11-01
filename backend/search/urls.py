from django.urls import path

from . import handler

urlpatterns = [
    path('search', handler.search),
    path('changePasswd', handler.change_passwd),
    path('setPasswd', handler.set_passwd),
    path('uploadArticle', handler.upload_article),
    path('uploadJournal', handler.upload_journal),
    path('modifyArticle', handler.modify_article),
    path('deleteArticle', handler.delete_article),
    path('deleteAll', handler.delete_all),
    path('requestContent', handler.request_content),
    path('login', handler.login),
    path('runningStatus', handler.running_status)
]