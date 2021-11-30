import pandas as pd
from searcher.qcm_cqg_searcher import QCMCQGSearcher
import config
from pyserini.search import get_topics

topics = get_topics('core17')

qcmcqg_kis_s6 = QCMCQGSearcher(path_idx=config.qcmcqg_kis_s6['PATH_IDX'],
                               path_bg_model=config.qcmcqg_kis_s6['BM'],
                               collection=config.qcmcqg_kis_s6['COLLECTION'],
                               topic_models_path=config.qcmcqg_kis_s6['TOPIC_MODELS'],
                               _lambda=config.qcmcqg_kis_s6['LAMBDA'])

qcmcqg_kis_s7 = QCMCQGSearcher(path_idx=config.qcmcqg_kis_s7['PATH_IDX'],
                               path_bg_model=config.qcmcqg_kis_s7['BM'],
                               collection=config.qcmcqg_kis_s7['COLLECTION'],
                               topic_models_path=config.qcmcqg_kis_s7['TOPIC_MODELS'],
                               _lambda=config.qcmcqg_kis_s7['LAMBDA'])

qcmcqg_kis_s8 = QCMCQGSearcher(path_idx=config.qcmcqg_kis_s8['PATH_IDX'],
                               path_bg_model=config.qcmcqg_kis_s8['BM'],
                               collection=config.qcmcqg_kis_s8['COLLECTION'],
                               topic_models_path=config.qcmcqg_kis_s8['TOPIC_MODELS'],
                               _lambda=config.qcmcqg_kis_s8['LAMBDA'])

qcmcqg_tts_s6 = QCMCQGSearcher(path_idx=config.qcmcqg_tts_s6['PATH_IDX'],
                               path_bg_model=config.qcmcqg_tts_s6['BM'],
                               collection=config.qcmcqg_tts_s6['COLLECTION'],
                               topic_models_path=config.qcmcqg_tts_s6['TOPIC_MODELS'],
                               _lambda=config.qcmcqg_tts_s6['LAMBDA'])

qcmcqg_tts_s7 = QCMCQGSearcher(path_idx=config.qcmcqg_tts_s7['PATH_IDX'],
                               path_bg_model=config.qcmcqg_tts_s7['BM'],
                               collection=config.qcmcqg_tts_s7['COLLECTION'],
                               topic_models_path=config.qcmcqg_tts_s7['TOPIC_MODELS'],
                               _lambda=config.qcmcqg_tts_s7['LAMBDA'])

qcmcqg_tts_s8 = QCMCQGSearcher(path_idx=config.qcmcqg_tts_s8['PATH_IDX'],
                               path_bg_model=config.qcmcqg_tts_s8['BM'],
                               collection=config.qcmcqg_tts_s8['COLLECTION'],
                               topic_models_path=config.qcmcqg_tts_s8['TOPIC_MODELS'],
                               _lambda=config.qcmcqg_tts_s8['LAMBDA'])

q_kis_s6 = None
q_kis_s7 = None
q_kis_s8 = None
q_tts_s6 = None
q_tts_s7 = None
q_tts_s8 = None

memory_kis_s6 = {}
memory_kis_s7 = {}
memory_kis_s8 = {}
memory_tts_s6 = {}
memory_tts_s7 = {}
memory_tts_s8 = {}

data = []

for topic in topics: 

    memory_kis_s6[topic] = []
    memory_kis_s7[topic] = []
    memory_kis_s8[topic] = []
    memory_tts_s6[topic] = []
    memory_tts_s7[topic] = []
    memory_tts_s8[topic] = []

    for rank in range(1, 11):
        query_candidates_kis_s6 = qcmcqg_kis_s6.get_query_candidates(topic=topic, q_init=q_kis_s6,
                                                                     offset_terms=config.qcmcqg_kis_s6['QCMCQG']['OFFSET_TERMS'],
                                                                     num_terms=config.qcmcqg_kis_s6['QCMCQG']['NUM_TERMS'],
                                                                     min_length=config.qcmcqg_kis_s6['QCMCQG']['MIN_LENGTH'],
                                                                     max_length=config.qcmcqg_kis_s6['QCMCQG']['MAX_LENGTH'],
                                                                     alpha=config.qcmcqg_kis_s6['QCMCQG']['ALPHA'],
                                                                     beta=config.qcmcqg_kis_s6['QCMCQG']['BETA'],
                                                                     epsilon=config.qcmcqg_kis_s6['QCMCQG']['EPSILON'],
                                                                     delta=config.qcmcqg_kis_s6['QCMCQG']['DELTA'],
                                                                     include_topic=config.qcmcqg_kis_s6['QCMCQG']['INCLUDE_TOPIC'],
                                                                     added_terms=config.qcmcqg_kis_s6['QCMCQG']['ADDED_TERMS'])

        query_candidates_kis_s7 = qcmcqg_kis_s7.get_query_candidates(topic=topic, q_init=q_kis_s7,
                                                                     offset_terms=config.qcmcqg_kis_s7['QCMCQG']['OFFSET_TERMS'],
                                                                     num_terms=config.qcmcqg_kis_s7['QCMCQG']['NUM_TERMS'],
                                                                     min_length=config.qcmcqg_kis_s7['QCMCQG']['MIN_LENGTH'],
                                                                     max_length=config.qcmcqg_kis_s7['QCMCQG']['MAX_LENGTH'],
                                                                     alpha=config.qcmcqg_kis_s7['QCMCQG']['ALPHA'],
                                                                     beta=config.qcmcqg_kis_s7['QCMCQG']['BETA'],
                                                                     epsilon=config.qcmcqg_kis_s7['QCMCQG']['EPSILON'],
                                                                     delta=config.qcmcqg_kis_s7['QCMCQG']['DELTA'],
                                                                     include_topic=config.qcmcqg_kis_s7['QCMCQG']['INCLUDE_TOPIC'],
                                                                     added_terms=config.qcmcqg_kis_s7['QCMCQG']['ADDED_TERMS'])

        query_candidates_kis_s8 = qcmcqg_kis_s8.get_query_candidates(topic=topic, q_init=q_kis_s8,
                                                                     offset_terms=config.qcmcqg_kis_s8['QCMCQG']['OFFSET_TERMS'],
                                                                     num_terms=config.qcmcqg_kis_s8['QCMCQG']['NUM_TERMS'],
                                                                     min_length=config.qcmcqg_kis_s8['QCMCQG']['MIN_LENGTH'],
                                                                     max_length=config.qcmcqg_kis_s8['QCMCQG']['MAX_LENGTH'],
                                                                     alpha=config.qcmcqg_kis_s8['QCMCQG']['ALPHA'],
                                                                     beta=config.qcmcqg_kis_s8['QCMCQG']['BETA'],
                                                                     epsilon=config.qcmcqg_kis_s8['QCMCQG']['EPSILON'],
                                                                     delta=config.qcmcqg_kis_s8['QCMCQG']['DELTA'],
                                                                     include_topic=config.qcmcqg_kis_s8['QCMCQG']['INCLUDE_TOPIC'],
                                                                     added_terms=config.qcmcqg_kis_s8['QCMCQG']['ADDED_TERMS'])

        query_candidates_tts_s6 = qcmcqg_tts_s6.get_query_candidates(topic=topic, q_init=q_tts_s6,
                                                                     offset_terms=config.qcmcqg_tts_s6['QCMCQG']['OFFSET_TERMS'],
                                                                     num_terms=config.qcmcqg_tts_s6['QCMCQG']['NUM_TERMS'],
                                                                     min_length=config.qcmcqg_tts_s6['QCMCQG']['MIN_LENGTH'],
                                                                     max_length=config.qcmcqg_tts_s6['QCMCQG']['MAX_LENGTH'],
                                                                     alpha=config.qcmcqg_tts_s6['QCMCQG']['ALPHA'],
                                                                     beta=config.qcmcqg_tts_s6['QCMCQG']['BETA'],
                                                                     epsilon=config.qcmcqg_tts_s6['QCMCQG']['EPSILON'],
                                                                     delta=config.qcmcqg_tts_s6['QCMCQG']['DELTA'],
                                                                     include_topic=config.qcmcqg_tts_s6['QCMCQG']['INCLUDE_TOPIC'],
                                                                     added_terms=config.qcmcqg_tts_s6['QCMCQG']['ADDED_TERMS'])

        query_candidates_tts_s7 = qcmcqg_tts_s7.get_query_candidates(topic=topic, q_init=q_tts_s7,
                                                                     offset_terms=config.qcmcqg_tts_s7['QCMCQG']['OFFSET_TERMS'],
                                                                     num_terms=config.qcmcqg_tts_s7['QCMCQG']['NUM_TERMS'],
                                                                     min_length=config.qcmcqg_tts_s7['QCMCQG']['MIN_LENGTH'],
                                                                     max_length=config.qcmcqg_tts_s7['QCMCQG']['MAX_LENGTH'],
                                                                     alpha=config.qcmcqg_tts_s7['QCMCQG']['ALPHA'],
                                                                     beta=config.qcmcqg_tts_s7['QCMCQG']['BETA'],
                                                                     epsilon=config.qcmcqg_tts_s7['QCMCQG']['EPSILON'],
                                                                     delta=config.qcmcqg_tts_s7['QCMCQG']['DELTA'],
                                                                     include_topic=config.qcmcqg_tts_s7['QCMCQG']['INCLUDE_TOPIC'],
                                                                     added_terms=config.qcmcqg_tts_s7['QCMCQG']['ADDED_TERMS'])

        query_candidates_tts_s8 = qcmcqg_tts_s8.get_query_candidates(topic=topic, q_init=q_tts_s8,
                                                                     offset_terms=config.qcmcqg_tts_s8['QCMCQG']['OFFSET_TERMS'],
                                                                     num_terms=config.qcmcqg_tts_s8['QCMCQG']['NUM_TERMS'],
                                                                     min_length=config.qcmcqg_tts_s8['QCMCQG']['MIN_LENGTH'],
                                                                     max_length=config.qcmcqg_tts_s8['QCMCQG']['MAX_LENGTH'],
                                                                     alpha=config.qcmcqg_tts_s8['QCMCQG']['ALPHA'],
                                                                     beta=config.qcmcqg_tts_s8['QCMCQG']['BETA'],
                                                                     epsilon=config.qcmcqg_tts_s8['QCMCQG']['EPSILON'],
                                                                     delta=config.qcmcqg_tts_s8['QCMCQG']['DELTA'],
                                                                     include_topic=config.qcmcqg_tts_s8['QCMCQG']['INCLUDE_TOPIC'],
                                                                     added_terms=config.qcmcqg_tts_s8['QCMCQG']['ADDED_TERMS'])

        for qc in query_candidates_kis_s6:
            if qc not in memory_kis_s6[topic]:
                q_kis_s6 = qc
                memory_kis_s6[topic].append(qc)
                break

        for qc in query_candidates_kis_s7:
            if qc not in memory_kis_s7[topic]:
                q_kis_s7 = qc
                memory_kis_s7[topic].append(qc)
                break

        for qc in query_candidates_kis_s8:
            if qc not in memory_kis_s8[topic]:
                q_kis_s8 = qc
                memory_kis_s8[topic].append(qc)
                break

        for qc in query_candidates_tts_s6:
            if qc not in memory_tts_s6[topic]:
                q_tts_s6 = qc
                memory_tts_s6[topic].append(qc)
                break

        for qc in query_candidates_tts_s7:
            if qc not in memory_tts_s7[topic]:
                q_tts_s7 = qc
                memory_tts_s7[topic].append(qc)
                break

        for qc in query_candidates_tts_s8:
            if qc not in memory_tts_s8[topic]:
                q_tts_s8 = qc
                memory_tts_s8[topic].append(qc)
                break

        data.append({'topic': topic,
                     'rank': rank,
                     'qcmcqg_kis_s6': q_kis_s6,
                     'qcmcqg_kis_s7': q_kis_s7,
                     'qcmcqg_kis_s8': q_kis_s8,
                     'qcmcqg_tts_s6': q_tts_s6,
                     'qcmcqg_tts_s7': q_tts_s7,
                     'qcmcqg_tts_s8': q_tts_s8})

pd.DataFrame(data).to_csv('data/queries/s678.csv', index=False)

