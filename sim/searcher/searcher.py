import os; os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64/"
from pyserini.search import get_topics, get_qrels
from pyserini.index import IndexReader
import pandas as pd
import json


class Searcher(object):

    def __init__(self, path_idx, path_bg_model, collection, _lambda, topic_models_path=None):
        self.index_reader = IndexReader(path_idx)
        self.N = self.index_reader.stats().get('documents')
        self.p_ml_corpus = pd.read_csv(path_bg_model, index_col=0)
        self.topics = get_topics(collection)
        self.qrels = get_qrels(collection)
        self._lambda = _lambda
        self.topic_models = None

        if topic_models_path:
            with open(topic_models_path) as f_in:
                self.topic_models = json.loads(f_in.read())

    def get_term_candidates(self, topic, _lambda):
        pass

    def get_query_candidates(self, topic, _lambda=None, strategy='s1'):

        if _lambda is None:
            _lambda = self._lambda

        term_candiates = self.get_term_candidates(topic=topic, _lambda=_lambda)

        if strategy == 's1':
            query_candidates = []
            for term in term_candiates.keys():
                query_candidates.append(term)

            return query_candidates

        if strategy == 's2':
            query_candidates = []
            terms = list(term_candiates.keys())
            t_0 = terms[0]
            for term in terms[1:]:
                query_candidates.append(' '.join([t_0, term]))

            return query_candidates

        if strategy == 's3':
            query_candidates = []
            terms = list(term_candiates.keys())
            t_0 = terms[0]
            t_1 = terms[1]
            for term in terms[2:]:
                query_candidates.append(' '.join([t_0, t_1, term]))

            return query_candidates

        if strategy == 's4':
            query_candidates = []
            terms = list(term_candiates.keys())
            t_0 = terms[0]
            query_candidates.append(t_0)
            for num, term in enumerate(terms[1:]):
                query_candidates.append(' '.join([query_candidates[num], term]))

            return query_candidates
            
        if strategy == 's5':
            query_candidates = []
            terms = list(term_candiates.keys())
            t_0 = terms[0]
            t_1 = terms[1]
            query_candidates.append(' '.join([t_0, t_1]))
            for num, term in enumerate(terms[2:]):
                query_candidates.append(' '.join([query_candidates[num], term]))

            return query_candidates
