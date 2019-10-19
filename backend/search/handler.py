from django.http import HttpResponse
from django.db.models import Q
from django.http import JsonResponse
from django.forms.models import model_to_dict

import json
import re
import jieba
import jieba.analyse

from .models import Passwd, Article, DictItem
from .rank import PageRank

filter_fulltext_score = 0.2
filter_keyword_score = 0.55

def mlist_convert(mlist):
    return [model_to_dict(x) for x in mlist]

def search_journal(journal):
    return mlist_convert(Article.objects.filter(journal=journal))

def search_db(text, limit):
    keys = re.sub('[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*·（）：；【】“”]+', '', text)
    keys = list(jieba.cut_for_search(keys))
    wset, results = set(), []
    for key in keys:
        for article in DictItem.objects.get(word=key).ids.all():
            if not article.id in wset:
                wset.add(article.id)
                results.append(model_to_dict(article))
    return PageRank().filter(keys, results, limit)

def word_filter(words):
    wset = set()
    for word in words:
        if not word.isspace():
            wset.add(word)
    words = []
    for word in wset:
        filtered = re.sub('[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*·（）：；【】“”]+', '', word)
        if len(filtered):
            words.append(filtered)
    return words

def get_words(title, content):
    title_words = jieba.cut_for_search(title)
    content_words = jieba.cut(content)
    return word_filter(list(title_words) + list(content_words))

def add_relationship_db(words, article):
    for word in words:
        try:
            item = DictItem.objects.get(word=word)
        except:
            item = DictItem(word=word)
            item.save()
        item.ids.add(article)
        item.save()

def delete_relationship_db(words, article):
    for word in words:
        item = DictItem.objects.get(word=word)
        item.ids.remove(article)
        item.save()

def add_article_db(journal, title, content):
    words = get_words(title, content)
    keys = jieba.analyse.extract_tags(content, topK=10)
    article = Article(journal=journal, title=title, content=content, keys='+'.join(keys))
    article.save()
    add_relationship_db(words, article)

def delete_article_db(id):
    article = Article.objects.get(id=id)
    words = get_words(article.title, article.content)
    delete_relationship_db(words, article)
    Article.objects.delete(id=id)

def modify_article_db(id, journal, title, content):
    article = Article.objects.get(id=id)
    words = get_words(article.title, article.content)
    delete_relationship_db(words, article)
    article.journal = journal
    article.title = title
    article.content = content
    article.keys = '+'.join(jieba.analyse.extract_tags(content, topK=10))
    article.save()
    words = get_words(title, content)
    add_relationship_db(words, article)

def modify_article(request):
    requestJson = json.loads(request.body)
    # try:
    modify_article_db(requestJson['id'], requestJson['journal'], requestJson['title'], requestJson['content'])
    # except:
    # return HttpResponse(json.dumps({'result': False}))
    return HttpResponse(json.dumps({'result': True}))

def delete_article(request):
    requestJson = json.loads(request.body)
    # try:
    delete_article_db(requestJson['id'])
    # except:
    # return HttpResponse(json.dumps({'result': False}))
    return HttpResponse(json.dumps({'result': True}))

def upload_article(request):
    requestJson = json.loads(request.body)
    # try:
    add_article_db(requestJson['journal'], requestJson['title'], requestJson['content'])
    # except:
        # return HttpResponse(json.dumps({'result': False}))
    return HttpResponse(json.dumps({'result': True}))

def search(request):
    requestJson = json.loads(request.body)
    text = requestJson['searchText']
    option = requestJson['searchOption']
    if option == 'journal':
        result = search_journal(text)
    elif option == 'fulltext':
        result = search_db(text, filter_fulltext_score)
    else:
        result = search_db(text, filter_keyword_score)
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