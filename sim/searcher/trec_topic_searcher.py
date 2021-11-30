import math
from collections import Counter
from sim.searcher.searcher import Searcher
from utils import sort_dict


class TRECTopicSearcher(Searcher):

    def __init__(self, **kwargs):
        super(TRECTopicSearcher, self).__init__(**kwargs)
        self.term_order = kwargs.get('term_order', None)

    def get_term_order(self):
        return self.term_order

    def set_term_order(self, term_order):
        if term_order is None or term_order in ['tfidf', 'cqg']:
            self.term_order = term_order
    
    def get_term_candidates(self, topic, _lambda=None):

        if _lambda is None:
            _lambda = self._lambda

        txt = ' '.join([self.topics.get(topic).get('title'),
                        self.topics.get(topic).get('description'),
                        self.topics.get(topic).get('narrative')])

        term_candidates = {}

        if self.term_order is None:

            terms = []
            for term in txt.split():
                analyzed_term = self.index_reader.analyze(term)
                if len(analyzed_term) > 0:
                    if analyzed_term[0] not in terms:
                        terms.append(analyzed_term[0])
            _norm = len(terms)
            _score = len(terms)
            for term in terms:
                term_candidates[term] = _score / _norm 
                _score -= 1

        if self.term_order == 'tfidf':

            term_candidates = Counter()
            for term in txt.split():
                analyzed_term = self.index_reader.analyze(term)
                if len(analyzed_term) > 0:
                    term_candidates.update({analyzed_term[0]: 1})

            for term in term_candidates:
                df, cf = self.index_reader.get_term_counts(term, analyzer=None)
                idf = math.log(1 + (self.N/df))
                term_candidates[term] = term_candidates[term] * idf

            term_candidates = sort_dict(term_candidates)

        if self.term_order == 'cqg':
            
            term_candidates = Counter()
            for term in txt.split():
                analyzed_term = self.index_reader.analyze(term)
                if len(analyzed_term) > 0:
                    term_candidates.update({analyzed_term[0]: 1})

            _sum = sum(term_candidates.values())
            p_ml = {k: v/_sum for k, v in term_candidates.items()}
            p_ml_corpus_prob = self.p_ml_corpus['prob'].to_dict()

            blacklist = ['null', 'nan']
            # _lambda = 0.4
            p_jm = {k: (1 - _lambda) * v + _lambda * p_ml_corpus_prob[k] for k, v in p_ml.items() if k not in blacklist and p_ml_corpus_prob.get(k) is not None}
            term_candidates = {k: v * math.log(v / p_ml_corpus_prob[k]) for k, v in p_jm.items()}
            term_candidates = sort_dict(term_candidates)

        return term_candidates
