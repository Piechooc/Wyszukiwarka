from DataHandler import DataHandler
import numpy as np
import scipy.sparse as ss
import scipy.sparse.linalg as ssl
import json


class SearchEngine:
    def __init__(self, data_size, name, idf=True, low_rank=False, k=0):
        self.name = name
        self.data_handler = DataHandler()
        if low_rank:
            self.data_handler.create_low_rank_dataset(data_size, idf, k)
        else:
            # self.data_handler.create_dataset(data_size, self.name, idf, low_rank, k)
            self.data_handler.load(self.name)

        print(f"Done {self.name}")

    def search(self, query):
        words = self.data_handler.prepare_text(query)

        q = ss.lil_matrix((1, len(self.data_handler.terms)), dtype=np.float32)
        for word in words:
            if word in self.data_handler.terms:
                q[0, self.data_handler.terms[word]] += 1

        q = q.tocsr()
        q_norm = ssl.norm(q)
        q /= q_norm

        temp = ss.find(q @ self.data_handler.tbd_matrix)
        indexes = temp[1]
        scores = temp[2]
        result = [(scores[i], indexes[i]) for i in range(len(indexes))]
        result.sort(reverse=True)

        max_articles = 0
        data = []
        for i in result:
            if max_articles == 10:
                break

            art = dict()
            art["title"] = self.data_handler.articles[i[1]].title
            art["link"] = self.data_handler.articles[i[1]].link
            art["body"] = self.data_handler.articles[i[1]].body[:1024]
            data.append(art)
            max_articles += 1

        with open('data.json', 'w') as f:
            json.dump(data, f)