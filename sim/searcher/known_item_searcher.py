from sim.searcher.searcher import Searcher
from collections import Counter
import math
from utils import sort_dict


class KnownItemSearcher(Searcher):

    def get_term_candidates(self, topic, _lambda=None):

        if _lambda is None:
            _lambda = self._lambda

        if(self.topic_models):
            return self.topic_models.get(str(_lambda)).get(str(topic))

        docids = [docid for docid, rel in self.qrels.get(topic).items() if int(rel) > 0]

        term_candidates = Counter()
        for docid in docids:
            _counter = Counter(self.index_reader.get_document_vector(str(docid)))
            term_candidates.update(_counter)

        _sum = sum(term_candidates.values())
        p_ml = {k: v/_sum for k, v in term_candidates.items()}

        p_ml_corpus_prob = self.p_ml_corpus['prob'].to_dict()
        blacklist = ['null', 'nan']

        p_jm = {k: (1 - _lambda) * v + _lambda * p_ml_corpus_prob[k] for k, v in p_ml.items() if k not in blacklist}
        score = {k: v * math.log(v / p_ml_corpus_prob[k]) for k, v in p_jm.items()}
        return sort_dict(score)
