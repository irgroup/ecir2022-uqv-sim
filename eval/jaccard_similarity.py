import os; os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64/"
import pandas as pd
import matplotlib.pyplot as plt

import numpy as np
import seaborn as sns

USER = 5
k = 1000
trec_measure = 'ndcg'

searcher = SimpleSearcher(config['PATH_IDX'])
index_reader = IndexReader(config['PATH_IDX'])
topics = get_topics('core17')
qrels = get_qrels('core17')

df_uqv = uqv()
df_trec = trec()
df_qcmcqg = qcmcqg()

rpd_eval = RpdEvaluator(qrel_orig_path=config['QREL'])

data = {}


def get_queries(sim, topic):
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
    return queries


def unique_terms(queries):
    concat = []
    for query in queries:
        concat = concat + index_reader.analyze(query)
    return set(concat)


def jaccard(ref,compare):
    overlap = ref & compare
    union = ref.union(compare)
    return len(overlap) / len(union)


simulators = ['uqv_1', 'uqv_2', 'uqv_3', 'uqv_4',
              'uqv_5', 'uqv_6', 'uqv_7', 'uqv_8',
              'tts_s1', 'tts_s2', 'tts_s3', 'tts_s4', 'tts_s5',
              'kis_s1', 'kis_s2', 'kis_s3', 'kis_s4', 'kis_s5',
              'qcmcqg_tts_s6', 'qcmcqg_tts_s7', 'qcmcqg_tts_s8',
              'qcmcqg_kis_s6', 'qcmcqg_kis_s7', 'qcmcqg_kis_s8']

for sim in simulators:

    _data = {}

    for topic in topics.keys():

        for vs in simulators:
            queries = get_queries(vs, topic)

            ref_queries = get_queries(sim, topic)
            ut_ref = unique_terms(ref_queries[:len(queries)])

            ut = unique_terms(queries)

            if _data.get(vs) is None:
                _data[vs] = [jaccard(ut_ref, ut)]
            else:
                _data[vs].append(jaccard(ut_ref, ut))

    for vs in simulators:
        _data[vs] = sum(_data[vs]) / len(_data[vs])

    data[sim] = _data

df = pd.DataFrame.from_dict(data)
df.to_csv('data/experimental_results/jacc.csv')
sns.heatmap(df, mask=np.triu(df), cmap="Blues", vmin=0)
plt.show()

########################################################################################################################
########################################################################################################################
df = pd.read_csv('data/experimental_results/jacc.csv', index_col=0)
df = df[['uqv_1', 'uqv_2', 'uqv_3', 'uqv_4',
         'uqv_5', 'uqv_6', 'uqv_7', 'uqv_8',
         'tts_s1', 'tts_s2', 'tts_s3', 'tts_s4', 'tts_s5',
         'qcmcqg_tts_s6', 'qcmcqg_tts_s7', 'qcmcqg_tts_s8',
         'kis_s1', 'kis_s2', 'kis_s3', 'kis_s4', 'kis_s5',
         'qcmcqg_kis_s6', 'qcmcqg_kis_s7', 'qcmcqg_kis_s8']]
df = df.loc[['uqv_1', 'uqv_2', 'uqv_3', 'uqv_4',
         'uqv_5', 'uqv_6', 'uqv_7', 'uqv_8',
         'tts_s1', 'tts_s2', 'tts_s3', 'tts_s4', 'tts_s5',
         'qcmcqg_tts_s6', 'qcmcqg_tts_s7', 'qcmcqg_tts_s8',
         'kis_s1', 'kis_s2', 'kis_s3', 'kis_s4', 'kis_s5',
         'qcmcqg_kis_s6', 'qcmcqg_kis_s7', 'qcmcqg_kis_s8']]
names = ['$\mathregular{UQV_1}$', '$\mathregular{UQV_2}$', '$\mathregular{UQV_3}$', '$\mathregular{UQV_4}$',
         '$\mathregular{UQV_5}$', '$\mathregular{UQV_6}$', '$\mathregular{UQV_7}$', '$\mathregular{UQV_8}$',
         '$\mathregular{TTS_{S1}}$','$\mathregular{TTS_{S2}}$','$\mathregular{TTS_{S2}\prime}$','$\mathregular{TTS_{S3}}$',
         '$\mathregular{TTS_{S3}\prime}$','$\mathregular{TTS_{S4}}$','$\mathregular{TTS_{S4}\prime}$','$\mathregular{TTS_{S4}\prime\prime}$',
         '$\mathregular{KIS_{S1}}$', '$\mathregular{KIS_{S2}}$', '$\mathregular{KIS_{S2}\prime}$', '$\mathregular{KIS_{S3}}$',
         '$\mathregular{KIS_{S3}\prime}$', '$\mathregular{KIS_{S4}}$', '$\mathregular{KIS_{S4}\prime}$', '$\mathregular{KIS_{S4}\prime\prime}$']
df.index = names
df.columns = names
ax = sns.heatmap(df, cmap=sns.color_palette("PuBu", as_cmap=True), linewidth=1, fmt="0.4f", mask=np.triu(df), vmin=0)
plt.title('Jaccard similarity between unique terms of the query strings')
plt.savefig('data/figures/jacc.pdf', bbox_inches='tight')
plt.show()
########################################################################################################################
########################################################################################################################