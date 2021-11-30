import os; os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64/"
import math
import pandas as pd
from utils import uqv, sort_dict
from pyserini.search import get_topics, get_qrels
from pyserini.index import IndexReader
from collections import Counter
from config import default as config
import json

qrels = get_qrels(config['COLLECTION'])
topics = get_topics(config['COLLECTION'])
index_reader = IndexReader(config['PATH_IDX'])
p_ml_corpus = pd.read_csv(config['BM'], index_col=0)

topic_models = {}


def main():
    for _lambda in [round(0.1 * i, 1) for i in range(0, 11)]:
        print(_lambda)
        topic_models[_lambda] = {}
        # for topic in list(topics.keys())[:3]:
        for topic in topics.keys():
            print(topic)
            docids = [docid for docid, rel in qrels.get(topic).items() if int(rel) > 0]

            term_candidates = Counter()
            for docid in docids:
                _counter = Counter(index_reader.get_document_vector(str(docid)))
                term_candidates.update(_counter)

            _sum = sum(term_candidates.values())
            p_ml = {k: v/_sum for k, v in term_candidates.items()}

            p_ml_corpus_prob = p_ml_corpus['prob'].to_dict()
            blacklist = ['null', 'nan']

            p_jm = {k: (1 - _lambda) * v + _lambda * p_ml_corpus_prob[k] for k, v in p_ml.items() if k not in blacklist}
            score = {k: v * math.log(v / p_ml_corpus_prob[k]) for k, v in p_jm.items()}
            topic_models[_lambda][topic] = sort_dict(score)

    with open('data/lm/cqg.json', 'w') as f_out:
        f_out.write(json.dumps(topic_models))


if __name__ == '__main__':
    main()
