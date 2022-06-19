from DataHandler import DataHandler
import numpy as np
import scipy.sparse as ss
import scipy.sparse.linalg as ssl


class SearchEngine:
    def __init__(self, data_size, name, idf=True, low_rank=False, k=0):
        self.name = name
        self.data_handler = DataHandler()
        self.data_handler.create_dataset(data_size, self.name, idf, low_rank, k)

    def search(self, query):
        self.data_handler.load(self.name)

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
        for i in result:
            if max_articles == 10:
                break

            max_articles += 1

        print(result)


test = SearchEngine(10000, "10k", idf=False)
# test.search("april")
