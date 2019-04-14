#-*-coding:utf-8-*-

import chardet
import logging, os, re
import jieba, jieba.analyse

from sqldb import SQLDB

class Importer:
    def __init__(self, db):
        self.db = db
        self.logger = logging.getLogger('Import')
        jieba.initialize()

    def filename(self, path):
        return os.path.basename(path).split('.')[0]

    def to_utf8(self, string):
        return string.encode('utf8').decode('utf8')

    def word_filter(self, words):
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
        title = self.filename(path)
        with open(path, 'r', encoding='gb18030') as f:
            content = f.read()
        content = self.to_utf8(content)
        self.from_raw(journal, title, content, False)

    def from_zip(self, path, multi):
        pass
    
    def from_dir(self, path, multi):
        if multi:
            for journal in os.listdir(path):
                jpath = os.path.join(path, journal)
                if os.path.isdir(jpath):
                    self.from_dir(jpath, False)
        else:
            journal = os.path.basename(path)
            for file in os.listdir(path):
                fpath = os.path.join(path, file)
                if os.path.isfile(fpath) and fpath.endswith('.txt'):
                    self.from_file(journal, fpath)



