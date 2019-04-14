#-*-coding:utf-8-*-

import logging, os, re, sqlite3
import jieba

from pagerank import PageRank

class SQLDB:
    def __init__(self, path, clean, commit_rate=50):
        self.db = None
        self.logger = logging.getLogger('SQLDB')
        if clean:
            if os.path.exists(path):
                os.remove(path)
                self.logger.info('Previous database has been deleted.')
        rebuild = not os.path.exists(path)
        try:
            self.db = sqlite3.connect(path)
        except:
            self.logger.error('Error while opening database.')
            exit(1)
        else:
            self.logger.info('Database opened successfully.')
        
        cursor = self.db.cursor()
        if rebuild:
            cursor.execute('CREATE TABLE pages (id int primary key, journal text, title text, content text, keys text)')
            cursor.execute('CREATE TABLE dicts (word text, id int)')
            self.index = 0
        else:
            self.index = cursor.execute('SELECT max(id) from pages').fetchone()[0]
            self.logger.info('The size of database if {}'.format(self.index))

        self.commit_rate = commit_rate
        self.commit_count = 0

    def search_init(self):
        jieba.initialize()
        self.pagerank = PageRank()

    def commit(self, show=True):
        self.db.commit()
        if show:
            self.logger.info('Database commit finished.')

    def flush(self):
        self.db.commit()
        self.db.close()
        self.logger.info('Database flushed.')

    def save(self, journal, title, content, words, keys, commit=False):
        self.index += 1
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO pages VALUES (?, ?, ?, ?, ?)", [self.index, journal, title, content, "+".join(keys)])
        for word in words:
            cursor.execute("INSERT INTO dicts VALUES (?, ?)", [word, self.index])
        info = '{} (Journal {})'.format(title, journal)
        self.logger.info('Saved {}, index will be {}.'.format(info, self.index))
        self.commit_count += 1
        if commit or self.commit_count % self.commit_rate == 0:
            self.commit()

    def search(self, keyword, sort=True):
        # search
        keys = re.sub('[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*·（）：；【】“”]+', '', keyword)
        self.logger.info('Get request for {}.'.format(keys))
        keys = list(jieba.cut_for_search(keys))
        cursor = self.db.cursor()
        cursor.execute('SELECT * from dicts WHERE word in ({})'.format(', '.join('?' for _ in keys)), keys)
        arts = set()
        for art in cursor.fetchall():
            arts.add(art[1])
        arts = list(arts)
        cursor.execute('SELECT * from pages WHERE id in ({})'.format(', '.join('?' for _ in arts)), arts)
        arts = cursor.fetchall()

        results = self.pagerank.sort(keys, arts)
        for art in results:
            print('Title: {}'.format(art[2]))
        return
        # pagerank
        if sort:
            return self.pagerank.sort(keys, arts)
        return arts

