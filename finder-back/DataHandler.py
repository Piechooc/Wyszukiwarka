import nltk
from datasets import load_dataset
import re
from unidecode import unidecode
from dataclasses import dataclass
import numpy as np
import scipy.sparse as ss
import scipy.sparse.linalg as ssl
import pickle
import os


@dataclass
class Article:
    title: str
    link: str
    body: str


class DataHandler:
    def __init__(self):
        nltk.download('wordnet')
        nltk.download('stopwords')
        nltk.download('punkt')
        nltk.download('omw-1.4')
        dateset_dict = load_dataset("wikipedia", "20220301.simple")
        self.dataset = dateset_dict['train']
        self.stop_words = set(nltk.corpus.stopwords.words('english'))
        self.stemmer = nltk.stem.porter.PorterStemmer()
        self.articles = None
        self.bags_of_words = None
        self.terms = None
        self.tbd_matrix = None
        self.create_folder()

    @staticmethod
    def create_folder():
        try:
            os.mkdir("./datasets")
        except FileExistsError:
            pass

    def create_dataset(self, articles_count, file_name, idf, low_rank, k):
        self.prepare_articles(articles_count)
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

    def prepare_articles(self, articles_count):
        self.articles = []
        self.bags_of_words = []
        self.terms = dict()

        all_terms = set()

        for i in range(articles_count):
            if i % 50 == 0:
                print(f"DONE {i}")

            words = dict()
            self.articles.append(Article(title=self.dataset["title"][i],
                                         link=self.dataset["url"][i], body=self.dataset["text"][i]))
            prepared_body = self.prepare_text(self.dataset["title"][i]) + self.prepare_text(self.dataset["text"][i])
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

    @staticmethod
    def pickle_dump(file_name, file_type, file):
        with open(f"./datasets/{file_type}_{file_name}", "wb") as file_type:
            pickle.dump(file, file_type)

    @staticmethod
    def pickle_load(file_name, file_type):
        with open(f"./datasets/{file_type}_{file_name}", "rb") as file_type:
            file = pickle.load(file_type)

        return file

    def save_dataset(self, file_name):
        self.pickle_dump(file_name, "articles", self.articles)
        self.pickle_dump(file_name, "bags_of_words", self.bags_of_words)
        self.pickle_dump(file_name, "terms", self.terms)
        self.pickle_dump(file_name, "tbd_matrix", self.tbd_matrix)

    def load(self, file_name):
        self.articles = self.pickle_load(file_name, "articles")
        self.bags_of_words = self.pickle_load(file_name, "bags_of_words")
        self.terms = self.pickle_load(file_name, "terms")
        self.tbd_matrix = self.pickle_load(file_name, "tbd_matrix")
