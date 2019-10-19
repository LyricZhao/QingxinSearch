from django.http import HttpResponse
from django.db.models import Q
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.http import HttpResponseBadRequest

import io
import json
import re
import jieba
import jieba.analyse
import zipfile
import chardet
import threading
import copy

from .models import Passwd, Article, DictItem
from .rank import PageRank

filter_fulltext_score = 0.2
filter_keyword_score = 0.55
db_is_running = False

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
        filtered = re.sub('[\s+\.\!\?\=\/_,$%^*(+\"\']+|[+——！，。？《》、~@#￥%……&*·（）：；【】“”]+', '', word)
        if len(filtered):
            words.append(filtered)
    return words

def get_words(title, content):
    title_words = jieba.cut_for_search(title)
    content_words = jieba.cut(content)
    return word_filter(list(title_words) + list(content_words))

def add_relationship_db(words, article):
    bulk_create_arr = []
    for word in words:
        if not DictItem.objects.filter(word=word).exists():
            bulk_create_arr.append(DictItem(word=word))
    DictItem.objects.bulk_create(bulk_create_arr)
    for word in words:
        item = DictItem.objects.get(word=word)
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

def add_articles_db(articles):
    word_set = set()
    word_map = {}
    word_bulk = []
    for article in articles:
        journal, title, content = article[0], article[1], article[2]
        keys = jieba.analyse.extract_tags(content, topK=10)
        article_word_set = set()
        for word in get_words(title, content):
            word_set.add(word)
            article_word_set.add(word)
        article_inst = Article(journal=journal, title=title, content=content, keys='+'.join(keys))
        article_inst.save()
        for word in article_word_set:
            if not word in word_map:
                word_map[word] = []
            word_map[word].append(article_inst)
    for word in word_set:
        if not DictItem.objects.filter(word=word).exists():
            word_bulk.append(DictItem(word=word))
    DictItem.objects.bulk_create(word_bulk)
    for word in word_set:
        item = DictItem.objects.get(word=word)
        item.ids.add(*word_map[word])
        item.save()

def delete_article_db(id):
    article = Article.objects.get(id=id)
    words = get_words(article.title, article.content)
    delete_relationship_db(words, article)
    article.delete()

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
    try:
        modify_article_db(requestJson['id'], requestJson['journal'], requestJson['title'], requestJson['content'])
    except:
        return HttpResponse(json.dumps({'result': False}))
    return HttpResponse(json.dumps({'result': True}))

def delete_article(request):
    requestJson = json.loads(request.body)
    try:
        delete_article_db(requestJson['id'])
    except:
        return HttpResponse(json.dumps({'result': False}))
    return HttpResponse(json.dumps({'result': True}))

def upload_article(request):
    requestJson = json.loads(request.body)
    try:
        add_article_db(requestJson['journal'], requestJson['title'], requestJson['content'])
    except:
        return HttpResponse(json.dumps({'result': False}))
    return HttpResponse(json.dumps({'result': True}))

def save_zip_into_db(zip_file):
    zip_file = io.BytesIO(zip_file)
    global db_is_running
    db_is_running = True
    articles = []
    with zipfile.ZipFile(zip_file, 'r') as zip:
        for filename in zip.namelist():
            original_filename = filename
            filename = filename.encode('cp437').decode('utf-8')
            if filename.startswith('_') or filename.startswith('.'):
                continue
            info = filename.split('/')
            if len(info) != 2:
                continue
            journal, title = info[0], info[1]
            if len(title) == 0:
                continue
            title = '.'.join(title.split('.')[0:-1])
            with zip.open(original_filename) as content:
                bytes_stream = content.read()
                if chardet.detect(bytes_stream)['encoding'] == 'utf-8':
                    content = bytes_stream.decode('utf-8')
                else:
                    content = bytes_stream.decode('gbk')
                articles.append((journal, title, content))
    add_articles_db(articles)
    db_is_running = False

def upload_journal(request):
    if db_is_running:
        raise HttpResponseBadRequest
    zip_file = request.FILES['file'].read()
    threading.Thread(target=save_zip_into_db, kwargs={'zip_file': zip_file}).start()
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

def delete_all(request):
    Article.objects.all().delete()
    DictItem.objects.all().delete()
    return HttpResponse('success')