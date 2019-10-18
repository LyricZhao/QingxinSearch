#-*-coding:utf-8-*-

class PageRank:
    def __init__(self):
        self.title_ratio = 0.4
        self.key_ratio = 0.4
        self.content_ratio = 0.2
        self.key_score = [20, 18, 16, 14, 4, 3, 2, 1, 1, 1]

    def get_key_score(self, keys, art_keys):
        score = 0
        art_keys = art_keys.split('+')
        for i in range(0, len(art_keys)):
            if art_keys[i] in keys:
                score += self.key_score[i]
        return score

    def get_similarity(self, keys, art):
        title_tot = content_tot = 0
        key_tot = len(keys)
        rkey_tot = min(self.get_key_score(keys, art[4]), key_tot)
        title, content = art[2], art[3]
        for key in keys:
            title_tot += title.count(key)
            content_tot += (content.count(key) > 0)
        return (self.title_ratio * title_tot + self.content_ratio * content_tot + self.key_ratio * rkey_tot) / (1.0 * key_tot)

    def filter(self, keys, arts, limit):
        results = []
        for i in range(len(arts)):
            sim = self.get_similarity(keys, arts[i])
            if sim > limit:
                results.append((sim, i))
        results.sort(reverse=True)
        results = [arts[result[1]] for result in results]
        return results