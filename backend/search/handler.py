from django.http import HttpResponse

import json

from .models import Passwd, Article, DictItem

def search(request):
    requestJson = json.loads(request.body)
    text = requestJson['searchText']
    option = int(requestJson['searchOption'])
    result = requestJson
    return HttpResponse(json.dumps(result), content_type='application/json')

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