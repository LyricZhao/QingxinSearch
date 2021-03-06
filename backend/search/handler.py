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

filter_fulltext_score = 0.1
filter_keyword_score = 0.55
db_is_running = False

def get_brief(text):
    if len(text) < 50:
        return text
    return text[0:48] + '...'

def get_model_dict(article):
    return {
        'journal': article.journal,
        'title': article.title,
        'brief': get_brief(article.text),
        'id': article.id
    }

def simplify(article):
    return {
        'journal': article['journal'],
        'title': article['title'],
        'brief': get_brief(article['text']),
        'id': article['id']
    }

def mlist_convert(mlist):
    return [get_model_dict(x) for x in mlist]

def search_journal(journal):
    try:
        return mlist_convert(Article.objects.filter(journal=journal))
    except:
        return []

def search_db(text, limit):
    keys = re.sub('[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*·（）：；【】“”]+', '', text)
    keys = list(jieba.cut_for_search(keys))
    wset, results = set(), []
    for key in keys:
        try:
            for article in DictItem.objects.get(word=key).ids.all():
                if not article.id in wset:
                    wset.add(article.id)
                    results.append(model_to_dict(article))
        except:
            pass
    sorted = PageRank().filter(keys, results, limit)
    return [simplify(article) for article in sorted]

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

def get_words(title, text):
    title_words = jieba.cut_for_search(title)
    text_words = jieba.cut(text)
    return word_filter(list(title_words) + list(text_words))

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

def add_article_db(journal, title, text, content):
    words = get_words(title, text)
    keys = jieba.analyse.extract_tags(text, topK=10)    
    article = Article(journal=journal, title=title, text=text, content=content, keys='+'.join(keys))
    article.save()
    add_relationship_db(words, article)

def add_articles_db(articles):
    word_set = set()
    word_map = {}
    word_bulk = []
    for article in articles:
        journal, title, text, content = article[0], article[1], article[2], article[2]
        keys = jieba.analyse.extract_tags(text, topK=10)
        article_word_set = set()
        for word in get_words(title, text):
            word_set.add(word)
            article_word_set.add(word)
        article_inst = Article(journal=journal, title=title, text=text, content=content, keys='+'.join(keys))
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
    words = get_words(article.title, article.text)
    delete_relationship_db(words, article)
    article.delete()

def modify_article_db(id, journal, title, text, content):
    article = Article.objects.get(id=id)
    words = get_words(article.title, article.text)
    delete_relationship_db(words, article)
    article.journal = journal
    article.title = title
    article.text = text
    article.content = content
    article.keys = '+'.join(jieba.analyse.extract_tags(text, topK=10))
    article.save()
    words = get_words(title, text)
    add_relationship_db(words, article)
    return get_model_dict(article)

def request_content_db(id):
    article = Article.objects.get(id=id)
    return article.content

def modify_article(request):
    if db_is_running:
        return HttpResponse(json.dumps({'result': False}))
    requestJson = json.loads(request.body)
    try:
        modified = modify_article_db(requestJson['id'], requestJson['journal'], requestJson['title'], requestJson['text'], requestJson['content'])
    except:
        return HttpResponse(json.dumps({'result': False}))
    return HttpResponse(json.dumps({'result': True, 'modified': modified}))

def delete_article(request):
    if db_is_running:
        return HttpResponse(json.dumps({'result': False}))
    requestJson = json.loads(request.body)
    try:
        delete_article_db(requestJson['id'])
    except:
        return HttpResponse(json.dumps({'result': False}))
    return HttpResponse(json.dumps({'result': True}))

def upload_article(request):
    if db_is_running:
        return HttpResponse(json.dumps({'result': False}))
    requestJson = json.loads(request.body)
    try:
        add_article_db(requestJson['journal'], requestJson['title'], requestJson['text'], requestJson['content'])
    except:
        return HttpResponse(json.dumps({'result': False}))
    return HttpResponse(json.dumps({'result': True}))

def request_content(request):
    requestJson = json.loads(request.body)
    try:
        content = request_content_db(requestJson['id'])
        return HttpResponse(json.dumps({'result': True, 'content': content}))
    except:
        return HttpResponse(json.dumps({'result': False}))

def save_zip_into_db(zip_file):
    try:
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
    except:
        pass

def upload_journal(request):
    if db_is_running:
        return HttpResponseBadRequest()
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
    except:
        return HttpResponse(json.dumps({'result': False}))
    return HttpResponse(json.dumps({'result': True}))

def set_passwd(request):
    passwd = request.GET['passwd']
    field = request.GET['field']
    if Passwd.objects.filter(id=field).exists():
        passwd_obj = Passwd.objects.get(id=field)
        passwd_obj.passwd = passwd
        passwd_obj.save()
    else:
        Passwd.objects.create(id=field, passwd=passwd)
    return HttpResponse('success')

def login(request):
    requestJson = json.loads(request.body)
    db_pass = requestJson['pass']
    try:
        if db_pass != Passwd.objects.get(id='db').passwd:
            return HttpResponse(json.dumps({'result': False}))
    except:
        return HttpResponse(json.dumps({'result': False}))
    return HttpResponse(json.dumps({'result': True})) 

def delete_all(request):
    if db_is_running:
        return HttpResponse('failed, running tasks')
    Article.objects.all().delete()
    DictItem.objects.all().delete()
    return HttpResponse('success')

def running_status(request):
    return HttpResponse(json.dumps({'result': db_is_running}))