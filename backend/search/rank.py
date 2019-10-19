#-*-coding:utf-8-*-

class PageRank:
    def __init__(self):
        self.title_ratio = 0.4
        self.key_ratio = 0.4
        self.content_ratio = 0.2
        self.key_score = [20, 18, 16, 14, 4, 3, 2, 1, 1, 1]

    def get_key_score(self, keys, article_keys):
        score = 0
        article_keys = article_keys.split('+')
        for i in range(len(article_keys)):
            if article_keys[i] in keys:
                score += self.key_score[i]
        return score

    def get_similarity(self, keys, article):
        title_tot = content_tot = 0
        key_tot = len(keys)
        rkey_tot = min(self.get_key_score(keys, article['keys']), key_tot)
        title, content = article['title'], article['content']
        for key in keys:
            title_tot += title.count(key)
            content_tot += (content.count(key) > 0)
        return (self.title_ratio * title_tot + self.content_ratio * content_tot + self.key_ratio * rkey_tot) / (1.0 * key_tot)

    def filter(self, keys, articles, limit):
        results = []
        for i in range(len(articles)):
            sim = self.get_similarity(keys, articles[i])
            if sim > limit:
                results.append((sim, i))
        results.sort(reverse=True)
        results = [articles[result[1]] for result in results]
        return results