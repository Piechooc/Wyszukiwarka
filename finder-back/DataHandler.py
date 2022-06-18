import nltk
import re
from unidecode import unidecode
from dataclasses import dataclass
import numpy as np
import scipy.sparse as ss
import scipy.sparse.linalg as ssl
import pickle


@dataclass
class Article:
    title: str
    link: str
    body: str


class DataHandler:
    def __init__(self):
        self.stop_words = set(nltk.corpus.stopwords.words('english'))
        self.stemmer = nltk.stem.porter.PorterStemmer()
        self.articles = None
        self.bags_of_words = None
        self.terms = None
        self.tbd_matrix = None

    def create_dataset(self, dataset, articles_count, file_name, idf, low_rank, k):
        self.prepare_articles(dataset, articles_count)
        print("===================== articles, bags, terms done =============================")
        if idf:
            self.do_idf(articles_count)
            print("=========================== idf done =================================")
        self.do_matrix()
        print("================================= matrix done ====================================")
        if low_rank:
            self.do_low_rank_approximation(k)
            print("=============================== low rank done ==============================")
        self.save_dataset(file_name)
        print("========================= DONE =========================")

    def prepare_text(self, text):
        text = re.sub(r'[^\w\s]', '', unidecode(text))
        text = re.sub(r'\d', '', text)
        tokens = [token for token in nltk.tokenize.word_tokenize(text.lower(), language='english')
                  if token not in self.stop_words and len(token) < 25]
        prepared_texts = [self.stemmer.stem(token) for token in tokens]

        return prepared_texts

    def prepare_articles(self, dataset, articles_count):
        self.articles = []
        self.bags_of_words = []
        self.terms = dict()

        all_terms = set()

        for i in range(articles_count):
            if i % 50 == 0:
                print(f"DONE {i}")

            words = dict()
            self.articles.append(Article(title=dataset["title"][i],
                                         link=dataset["url"][i], body=dataset["text"][i]))
            prepared_body = self.prepare_text(dataset["title"][i]) + self.prepare_text(dataset["text"][i])
            if i % 50 == 0:
                print(prepared_body)

            for word in prepared_body:
                if word in words:
                    words[word] += 1
                else:
                    words[word] = 1

            self.bags_of_words.append(words)
            all_terms.update(prepared_body)

        for index, word in enumerate(all_terms):
            self.terms[word] = index

    def do_idf(self, n):
        idf = np.zeros(len(self.terms))
        for bag in self.bags_of_words:
            for word in bag:
                idf[self.terms[word]] += 1

        idf = np.log(np.full(len(self.terms), n) / idf)

        for bag in self.bags_of_words:
            for word in bag:
                bag[word] *= idf[self.terms[word]]

    def do_matrix(self):
        tbd = ss.lil_matrix((len(self.terms), len(self.articles)), dtype=np.float32)

        for i, bag in enumerate(self.bags_of_words):
            d = np.array(list(bag.values()), dtype=np.float32)
            d /= np.linalg.norm(d)
            indexes = np.array([self.terms[word] for word in bag.keys()])
            tbd[indexes, i] = d

        self.tbd_matrix = tbd.tocsr()

    def do_low_rank_approximation(self, k):
        u, s, vt = ssl.svds(self.tbd_matrix, k=k)
        self.tbd_matrix = u @ s @ vt

    def save_dataset(self, file_name):
        with open(f"./datasets/articles_{file_name}", "wb") as articles:
            pickle.dump(self.articles, articles)

        with open(f"./datasets/bags_of_words_{file_name}", "wb") as bags_of_words:
            pickle.dump(self.bags_of_words, bags_of_words)

        with open(f"./datasets/terms_{file_name}", "wb") as terms:
            pickle.dump(self.terms, terms)

        with open(f"./datasets/tbd_matrix_{file_name}", "wb") as tbd_matrix:
            pickle.dump(self.tbd_matrix, tbd_matrix)

    def load_dataset(self, file_name):
        with open(f"./datasets/articles_{file_name}", "rb") as articles:
            self.articles = pickle.load(articles)

        with open(f"./datasets/bags_of_words_{file_name}", "rb") as bags_of_words:
            self.bags_of_words = pickle.load(bags_of_words)

        with open(f"./datasets/terms_{file_name}", "rb") as terms:
            self.terms = pickle.load(terms)

        with open(f"./datasets/tbd_matrix_{file_name}", "rb") as tbd_matrix:
            self.tbd_matrix = pickle.load(tbd_matrix)
