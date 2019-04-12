#-*-coding:utf-8-*-

import chardet
import logging, os, re
import jieba

from sqldb import SQLDB

class Importer:
    def __init__(self, db):
        self.db = db
        self.logger = logging.getLogger('Import')
        jieba.initialize()

    def to_utf8(self, string):
        encoding = chardet.detect(string)['encoding']
        return string.decode(encoding).encoding('utf-8')

    def word_filter(self, words):
        wset = set()
        for word in words:
            if not word.isspace():
                wset.add(word)
        words = []
        for word in wset:
            filtered = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*·（）：；【】“”]+".decode("utf8"), "".decode("utf8"), word)
            if len(filtered):
                words.append(filtered)
        return words

    def from_raw(self, journal, title, content, commit=False):
        if len(title) == 0 or len(content) == 0:
            self.logger.error('Invalid content, title: {}, content: {}'.format(title, content))
            return
        title_words = jieba.cut_for_search(title)
        content_words = jieba.cut(content)
        words = self.word_filter(list(title_words) + list(content_words))
        keys = jieba.analyse.extract_tags(content, topK=10)
        self.db.save(journal, title, content, words, keys, commit)

    def from_file(self, journal, path):
        with open(path, 'r') as f:
            title = f.readline()
            content = f.read()
        title = self.to_utf8(title)
        content = self.to_utf8(content)
        self.from_raw(journal, title, content, False)

    def from_zip(self, path, multi):
        pass
    
    def from_dir(self, path, multi):
        if multi:
            for journal in os.listdir(path):
                self.from_dir(os.path.join(path, journal), False)
        else:
            journal = os.path.basename(path)
            for file in os.listdir(path):
                self.from_file(journal, os.path.join(path, file))



