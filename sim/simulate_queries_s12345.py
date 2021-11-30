import pandas as pd
from searcher.trec_topic_searcher import TRECTopicSearcher
from searcher.known_item_searcher import KnownItemSearcher
from config import default as config
from pyserini.search import get_topics

topics = get_topics('core17')
 
tts = TRECTopicSearcher(path_idx=config['PATH_IDX'], 
                        path_bg_model=config['BM'], 
                        collection=config['COLLECTION'],
                        topic_models_path=config['TOPIC_MODELS'],
                        _lambda=config['LAMBDA'])

tts_tfidf = TRECTopicSearcher(path_idx=config['PATH_IDX'], 
                              path_bg_model=config['BM'], 
                              collection=config['COLLECTION'],
                              topic_models_path=config['TOPIC_MODELS'],
                              _lambda=config['LAMBDA'])

kis = KnownItemSearcher(path_idx=config['PATH_IDX'], 
                        path_bg_model=config['BM'], 
                        collection=config['COLLECTION'],
                        topic_models_path=config['TOPIC_MODELS'],
                        _lambda=config['LAMBDA'])

tts_tfidf.set_term_order('tfidf')

data = []

for strategy in ['s1', 's2', 's3', 's4', 's5']:

    for topic in topics.keys():
        qc_tts = tts.get_query_candidates(topic=topic, strategy=strategy)
        qc_tts_tfidf = tts_tfidf.get_query_candidates(topic=topic, strategy=strategy)
        qc_kis = kis.get_query_candidates(topic=topic, strategy=strategy)

        for rank in range(1, 11):
            data.append({'topic': topic,
                         'strategy': strategy,
                         'rank': rank,
                         'tts': qc_tts[rank-1],
                         'tts_tfidf': qc_tts_tfidf[rank-1],
                         'kis': qc_kis[rank-1]})

pd.DataFrame(data).to_csv('data/queries/s12345.csv', index=False)
