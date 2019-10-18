from django.http import HttpResponse

import json

def search(request):
    requestJson = json.loads(request.body)
    text = requestJson['searchText']
    option = int(requestJson['searchOption'])
    result = requestJson
    return HttpResponse(json.dumps(result), content_type='application/json')