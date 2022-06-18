import nltk
from datasets import load_dataset
from DataHandler import DataHandler
import numpy as np
import scipy.sparse as ss
import scipy.sparse.linalg as ssl


class SearchEngine:
    def __init__(self, data_size, name, idf=True, low_rank=False, k=0):
        nltk.download('wordnet')
        nltk.download('stopwords')
        nltk.download('punkt')
        nltk.download('omw-1.4')
        dateset_dict = load_dataset("wikipedia", "20220301.simple")
        self.name = name
        self.dataset = dateset_dict['train']
        self.data_handler = DataHandler()
        self.data_handler.create_dataset(self.dataset, data_size, self.name, idf, low_rank, k)

    def search(self, query):
        self.data_handler.load_dataset(self.name)

        words = self.data_handler.prepare_text(query)

        q = ss.lil_matrix((1, len(self.data_handler.terms)), dtype=np.float32)
        for word in words:
            if word in self.data_handler.terms:
                q[0, self.data_handler.terms[word]] += 1

        q = q.tocsr()
        q_norm = np.linalg.norm(q)
        q /= q_norm

        result = []

        for i in range(len(self.data_handler.articles)):
            result.append((self.data_handler.tbd_matrix.getcol(i).dot(q[0]) /
                           ssl.norm(self.data_handler.tbd_matrix.getcol(i)))[0])

        result = np.argsort(result)[-10:][::-1]

        for i in result:
            print(self.data_handler.articles[i].title)


test = SearchEngine(2000, "2k")
test.search("dog")
