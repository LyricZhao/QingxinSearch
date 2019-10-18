from django.http import HttpResponse
from django.db.models import Q

import json

from .models import Passwd, Article, DictItem

def search_journal(journal):
    return Article.objects.filter(Q(journal__contains=journal))

def search_fulltext():
    pass

def search_keyword():
    pass

def search(request):
    requestJson = json.loads(request.body)
    text = requestJson['searchText']
    option = requestJson['searchOption']
    if option == 'journal':
        result = search_journal(text)
    elif option == 'fulltext':
        result = search_fulltext(text)
    else:
        result = search_keyword(text)
    return HttpResponse(json.dumps({'result': result}), content_type='application/json')

def change_passwd(request):
    requestJson = json.loads(request.body)
    admin_pass = requestJson['adminPass']
    new_pass = requestJson['newPass']
    try:
        if admin_pass != Passwd.objects.get(id='admin').passwd:
            return HttpResponse(json.dumps({'result': False}))
        db_pass = Passwd.objects.get(id='db')
        db_pass.passwd = new_pass
        db_pass.save()
        return HttpResponse(json.dumps({'result': True}))
    except:
        return HttpResponse(json.dumps({'result': False}))

def set_passwd(request):
    passwd = request.GET['passwd']
    field = request.GET['field']
    try:
        passwd_obj = Passwd.objects.get(id=field)
        passed_obj.passwd = passwd
        passwd_obj.save()
    except:
        Passwd.objects.create(id=field, passwd=passwd)
    return HttpResponse('success')