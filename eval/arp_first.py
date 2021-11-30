from repro_eval.Evaluator import RpdEvaluator
import os; os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64/"
from pyserini.search import SimpleSearcher, get_topics, get_qrels
import pandas as pd

from utils import uqv, qcmcqg, trec, parse_results
from config import default as config
from tqdm import tqdm

USER = 5
k = 1000
trec_measure = 'ndcg'

searcher = SimpleSearcher(config['PATH_IDX'])
topics = get_topics('core17')
qrels = get_qrels('core17')

df_uqv = uqv()
df_trec = trec()
df_qcmcqg = qcmcqg()

rpd_eval = RpdEvaluator(qrel_orig_path=config['QREL'])

data = {}

for sim in tqdm(['uqv_1', 'uqv_2', 'uqv_3', 'uqv_4', 'uqv_5', 'uqv_6', 'uqv_7', 'uqv_8',
                 'tts_s1', 'tts_s2', 'tts_s3', 'tts_s4', 'tts_s5', 'kis_s1', 'kis_s2', 'kis_s3', 'kis_s4', 'kis_s5',
                 'qcmcqg_tts_s6', 'qcmcqg_tts_s7', 'qcmcqg_tts_s8', 'qcmcqg_kis_s6', 'qcmcqg_kis_s7', 'qcmcqg_kis_s8']):

    _data = {}

    _data['queries'] = 50
    _data['ndcg'] = 0.0
    _data['P_10'] = 0.0
    _data['map'] = 0.0

    number_of_queries = 0

    scores = {'ndcg': [],
              'P_10': [],
              'map': []}

    for topic in topics.keys():

        if sim == 'uqv_1':
            queries = list(df_uqv[(df_uqv['topic'] == topic) & (df_uqv['user'] == 1)]['qstr'])
        if sim == 'uqv_2':
            queries = list(df_uqv[(df_uqv['topic'] == topic) & (df_uqv['user'] == 2)]['qstr'])
        if sim == 'uqv_3':
            queries = list(df_uqv[(df_uqv['topic'] == topic) & (df_uqv['user'] == 3)]['qstr'])
        if sim == 'uqv_4':
            queries = list(df_uqv[(df_uqv['topic'] == topic) & (df_uqv['user'] == 4)]['qstr'])
        if sim == 'uqv_5':
            queries = list(df_uqv[(df_uqv['topic'] == topic) & (df_uqv['user'] == 5)]['qstr'])
        if sim == 'uqv_6':
            queries = list(df_uqv[(df_uqv['topic'] == topic) & (df_uqv['user'] == 6)]['qstr'])
        if sim == 'uqv_7':
            queries = list(df_uqv[(df_uqv['topic'] == topic) & (df_uqv['user'] == 7)]['qstr'])
        if sim == 'uqv_8':
            queries = list(df_uqv[(df_uqv['topic'] == topic) & (df_uqv['user'] == 8)]['qstr'])
        if sim == 'kis_s1':
            queries = list(df_trec[(df_trec['strategy'] == 's1') & (df_trec['topic'] == topic)]['kis'])
        if sim == 'kis_s2':
            queries = list(df_trec[(df_trec['strategy'] == 's2') & (df_trec['topic'] == topic)]['kis'])
        if sim == 'kis_s3':
            queries = list(df_trec[(df_trec['strategy'] == 's3') & (df_trec['topic'] == topic)]['kis'])
        if sim == 'kis_s4':
            queries = list(df_trec[(df_trec['strategy'] == 's4') & (df_trec['topic'] == topic)]['kis'])
        if sim == 'kis_s5':
            queries = list(df_trec[(df_trec['strategy'] == 's5') & (df_trec['topic'] == topic)]['kis'])
        if sim == 'tts_s1':
            queries = list(df_trec[(df_trec['strategy'] == 's1') & (df_trec['topic'] == topic)]['tts'])
        if sim == 'tts_s2':
            queries = list(df_trec[(df_trec['strategy'] == 's2') & (df_trec['topic'] == topic)]['tts'])
        if sim == 'tts_s3':
            queries = list(df_trec[(df_trec['strategy'] == 's3') & (df_trec['topic'] == topic)]['tts'])
        if sim == 'tts_s4':
            queries = list(df_trec[(df_trec['strategy'] == 's4') & (df_trec['topic'] == topic)]['tts'])
        if sim == 'tts_s5':
            queries = list(df_trec[(df_trec['strategy'] == 's5') & (df_trec['topic'] == topic)]['tts'])
        if sim == 'qcmcqg_kis_s6':
            queries = list(df_qcmcqg[df_qcmcqg['topic'] == topic]['qcmcqg_kis_s6'])
        if sim == 'qcmcqg_kis_s7':
            queries = list(df_qcmcqg[df_qcmcqg['topic'] == topic]['qcmcqg_kis_s7'])
        if sim == 'qcmcqg_kis_s8':
            queries = list(df_qcmcqg[df_qcmcqg['topic'] == topic]['qcmcqg_kis_s8'])
        if sim == 'qcmcqg_tts_s6':
            queries = list(df_qcmcqg[df_qcmcqg['topic'] == topic]['qcmcqg_tts_s6'])
        if sim == 'qcmcqg_tts_s7':
            queries = list(df_qcmcqg[df_qcmcqg['topic'] == topic]['qcmcqg_tts_s7'])
        if sim == 'qcmcqg_tts_s8':
            queries = list(df_qcmcqg[df_qcmcqg['topic'] == topic]['qcmcqg_tts_s8'])

        for query in queries[:1]:
            results = searcher.search(q=query, k=k)
            scores['ndcg'].append(
                rpd_eval.rel_eval.evaluate(parse_results(results, topic=str(topic))).get(str(topic)).get('ndcg'))
            scores['P_10'].append(
                rpd_eval.rel_eval.evaluate(parse_results(results, topic=str(topic))).get(str(topic)).get('P_10'))
            scores['map'].append(
                rpd_eval.rel_eval.evaluate(parse_results(results, topic=str(topic))).get(str(topic)).get('map'))
            number_of_queries += 1

        _data['queries'] = number_of_queries
        _data['ndcg'] = sum(scores['ndcg']) / len(scores['ndcg'])
        _data['P_10'] = sum(scores['P_10']) / len(scores['P_10'])
        _data['map'] = sum(scores['map']) / len(scores['map'])
        data[sim] = _data

pd.DataFrame.from_dict(data).to_csv('data/experimental_results/arp_first.csv')
