from sim.searcher.known_item_searcher import KnownItemSearcher
import itertools
import math
from utils import sort_dict
from collections import Counter


class QCMCQGSearcher(KnownItemSearcher):

    def precompute_topic_models(topics):
        pass

    def get_term_candidates(self, topic, include_topic=False, _lambda=None, added_terms=10):

        if _lambda is None:
            _lambda = self._lambda

        if(self.topic_models):
            if not include_topic:
                return self.topic_models.get(str(_lambda)).get(str(topic))

            precomputed_topic_model = self.topic_models.get(str(_lambda)).get(str(topic))

            to_be_returned = {}

            txt = ' '.join([self.topics.get(topic).get('title'),
                            self.topics.get(topic).get('description'),
                            self.topics.get(topic).get('narrative')])
            for term in txt.split():
                analyzed_term = self.index_reader.analyze(term)
                if len(analyzed_term) > 0:
                    if analyzed_term[0] not in ['document', 'relev', 'identifi']:
                        if precomputed_topic_model.get(analyzed_term[0]) is not None and to_be_returned.get(analyzed_term[0]) is None:
                            to_be_returned[analyzed_term[0]] = precomputed_topic_model.get(analyzed_term[0])

            cnt = 0
            for term in precomputed_topic_model.keys():
                if to_be_returned.get(term) is None:
                    to_be_returned[term] = precomputed_topic_model.get(term)
                    cnt += 1
                    if cnt == added_terms:
                        return sort_dict(to_be_returned)

        docids = [docid for docid, rel in self.qrels.get(topic).items() if int(rel) > 0]

        term_candidates = Counter()
        for docid in docids:
            _counter = Counter(self.index_reader.get_document_vector(str(docid)))
            term_candidates.update(_counter)

        if include_topic:
            txt = ' '.join([self.topics.get(topic).get('title'),
                            self.topics.get(topic).get('description'),
                            self.topics.get(topic).get('narrative')])

            for term in txt.split():
                analyzed_term = self.index_reader.analyze(term)
                if len(analyzed_term) > 0:
                    term_candidates.update({analyzed_term[0]: 1})

        _sum = sum(term_candidates.values())
        p_ml = {k: v/_sum for k, v in term_candidates.items()}

        p_ml_corpus_prob = self.p_ml_corpus['prob'].to_dict()
        blacklist = ['null', 'nan']
  
        p_jm = {k: (1 - _lambda) * v + _lambda * p_ml_corpus_prob[k] for k, v in p_ml.items() if k not in blacklist}
        score = {k: v * math.log(v / p_ml_corpus_prob[k]) for k, v in p_jm.items()}
        return sort_dict(score)

    def get_query_candidates(self, topic, q_init=None, **kwargs):

        self.offset_terms = kwargs.get('offset_terms', 0)
        self.num_terms = kwargs.get('num_terms', 20)
        self.min_length = kwargs.get('min_length', 3)
        self.max_length = kwargs.get('max_length', 5)
        self.alpha = kwargs.get('alpha', 2.2)               # account theme terms    
        self.beta = kwargs.get('beta', 1.8)                 # discount new TOPIC terms  
        self.epsilon = kwargs.get('epsilon', 0.07)          # account new terms 
        self.delta = kwargs.get('delta', 0.4)               # discount removed terms
        self.include_topic = kwargs.get('include_topic', False) 
        self._lambda = kwargs.get('_lambda', self._lambda)
        self.added_terms = kwargs.get('added_terms', 10)

        term_candidates = self.get_term_candidates(topic=topic, include_topic=self.include_topic, _lambda=self._lambda, added_terms=self.added_terms)
        query_candidates = []
        for length in range(self.min_length, self.max_length + 1):
            for subset in itertools.combinations(list(term_candidates.keys())[self.offset_terms:self.offset_terms + self.num_terms], length):
                query_candidates.append(' '.join(subset))

        if q_init is None:
            q_init_tokens = [self.index_reader.analyze(term)[0] for term in self.topics.get(topic).get('title').split() if len(self.index_reader.analyze(term)) > 0]     
        else: 
            q_init_tokens = [self.index_reader.analyze(term)[0] for term in q_init.split() if len(self.index_reader.analyze(term)) > 0]

        topic_txt = ' '.join([self.topics.get(topic).get('title'),
                              self.topics.get(topic).get('description'),
                              self.topics.get(topic).get('narrative')])
        topic_tokens = [self.index_reader.analyze(term)[0] for term in topic_txt.split() if len(self.index_reader.analyze(term)) > 0 ] 

        qc_scores = {}

        q_title_tokens = [self.index_reader.analyze(term)[0] for term in self.topics.get(topic).get('title').split() if
                         len(self.index_reader.analyze(term)) > 0]

        for qc in query_candidates:
            theme_tokens = set(q_title_tokens).intersection(set(qc.split()))
            add_tokens = set(qc.split()).difference(set(q_init_tokens))
            add_tokens_topic = set(add_tokens).intersection(set(topic_tokens))
            add_tokens_oot = set(add_tokens).difference(set(topic_tokens))
            rm_tokens = set(q_init_tokens).difference(set(qc.split()))

            _score = 0
            _norm = 0

            for tt in list(theme_tokens):
                _score = _score + (self.alpha * (1 - term_candidates.get(tt)))

            for att in list(add_tokens_topic):
                _score = _score + (1 - self.beta * term_candidates.get(att))

            for atoot in list(add_tokens_oot):
                df, cf = self.index_reader.get_term_counts(atoot, analyzer=None)
                _idf = math.log(1 + (self.N/df))
                _score = _score + (self.epsilon * _idf)

            for rt in list(rm_tokens):
                if term_candidates.get(rt) is not None: 
                    _score = _score - (self.delta * term_candidates.get(rt))

            _score = _score / len(qc.split())
            qc_scores[qc] = _score

        return list(sort_dict(qc_scores).keys())
