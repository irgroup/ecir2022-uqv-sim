import os; os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64/"
from pyserini.search import SimpleSearcher, get_topics, get_qrels
import pandas as pd
import matplotlib.pyplot as plt
from utils import uqv, qcmcqg, trec
from config import default as config
import math

import seaborn as sns
sns.set_style('darkgrid')


def cg(results, topic):
    _cg = 0
    for result in results:
       if qrels.get(topic).get(int(result.docid)) is not None:
           _cg += int(qrels.get(topic).get(int(result.docid)))
    return _cg


def dcg(results, topic):
    _dcg = 0

    for i, result in enumerate(results):
       if qrels.get(topic).get(int(result.docid)) is not None:
           _dcg += int(qrels.get(topic).get(int(result.docid))) / (1 + math.log(i+1, b))
    return _dcg


USER = 5
# k = 50
_q = 5
# topic = 336
trec_measure = 'ndcg'
b = 2
bq = 4

searcher = SimpleSearcher(config['PATH_IDX'])
topics = get_topics('core17')
qrels = get_qrels('core17')

df_uqv = uqv()
df_trec = trec()
df_qcmcqg = qcmcqg()

data = {}

for sim in ['uqv_5', 'tts_s3', 'kis_s3', 'qcmcqg_tts_s6', 'qcmcqg_tts_s7', 'qcmcqg_tts_s8']:
    _data = {}
    for k in list(range(1, 10, 1)) + list(range(10, 110, 10)):
        run = {}
        for topic in topics.keys():
            sdcg = 0.0

            if sim == 'uqv_5':
                queries = list(df_uqv[(df_uqv['topic'] == topic) & (df_uqv['user'] == USER)]['qstr'])[:_q]
            if sim == 'kis_s3':
                queries = list(df_trec[(df_trec['strategy'] == 's3') & (df_trec['topic'] == topic)]['kis'])[:_q]
            if sim == 'tts_s3':
                queries = list(df_trec[(df_trec['strategy'] == 's3') & (df_trec['topic'] == topic)]['tts'])[:_q]
            if sim == 'qcmcqg_tts_s6':
                queries = list(df_qcmcqg[df_qcmcqg['topic'] == topic]['qcmcqg_tts_s6'])[:_q]
            if sim == 'qcmcqg_tts_s7':
                queries = list(df_qcmcqg[df_qcmcqg['topic'] == topic]['qcmcqg_tts_s7'])[:_q]
            if sim == 'qcmcqg_tts_s8':
                queries = list(df_qcmcqg[df_qcmcqg['topic'] == topic]['qcmcqg_tts_s8'])[:_q]

            for q, query in enumerate(queries):
                results = searcher.search(q=query, k=k)
                sdcg += dcg(results, topic) / (1 + math.log(q + 1, bq))
            run[topic] = sdcg

        avg_sdcg = sum([sdcg for sdcg in run.values()])/len(topics)
        print(avg_sdcg)
        _data[k] = avg_sdcg

    data[sim] = _data

pd.DataFrame.from_dict(data).to_csv('data/experimental_results/sdcg_5queries.csv')
ax = pd.DataFrame.from_dict(data).plot()
ax.set_xlabel("Documents per query")
ax.set_ylabel('sDCG')
plt.title("sDCG (b=2, bq=4) with 5 queries")
plt.savefig('sdcg_5queries.pdf', bbox_inches='tight')
plt.show()

########################################################################################################################
########################################################################################################################
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')

_fs = (4,4)

df = pd.read_csv('data/experimental_results/sdcg_3queries.csv', index_col=0)
ax = df.plot(figsize=_fs)
ax.legend(['$\mathregular{UQV_{5}}$', '$\mathregular{TTS_{S2}\prime}$', '$\mathregular{KIS_{S2}\prime}$',
           '$\mathregular{TTS_{S4}}$','$\mathregular{TTS_{S4}\prime}$', '$\mathregular{TTS_{S4}\prime\prime}$'],
          loc='upper left', fontsize=12)
ax.set_xlabel("Documents per query")
ax.set_ylabel('sDCG')
ax.set_ylim(0, 60)
plt.title("sDCG (b=2, bq=4) with 3 queries")
plt.savefig('notes/figures/sdcg_3queries.pdf', bbox_inches='tight')
plt.show()
########################################################################################################################
########################################################################################################################
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')

df = pd.read_csv('data/experimental_results/sdcg_5queries.csv', index_col=0)
ax = df.plot(figsize=_fs)
ax.legend(['$\mathregular{UQV_{5}}$', '$\mathregular{TTS_{S2}\prime}$', '$\mathregular{KIS_{S2}\prime}$',
           '$\mathregular{TTS_{S4}}$','$\mathregular{TTS_{S4}\prime}$', '$\mathregular{TTS_{S4}\prime\prime}$'],
          loc='upper left', fontsize=12)
ax.set_xlabel("Documents per query")
ax.set_ylabel('sDCG')
ax.set_ylim(0, 60)
plt.title("sDCG (b=2, bq=4) with 5 queries")
plt.savefig('notes/figures/sdcg_5queries.pdf', bbox_inches='tight')
plt.show()
########################################################################################################################
########################################################################################################################
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')

df = pd.read_csv('data/experimental_results/sdcg_10queries.csv', index_col=0)
ax = df.plot(figsize=_fs)
ax.legend(['$\mathregular{UQV_{5}}$', '$\mathregular{TTS_{S2}\prime}$', '$\mathregular{KIS_{S2}\prime}$',
           '$\mathregular{TTS_{S4}}$','$\mathregular{TTS_{S4}\prime}$', '$\mathregular{TTS_{S4}\prime\prime}$'],
          loc='upper left', fontsize=12)
ax.set_xlabel("Documents per query")
ax.set_ylabel('sDCG')
ax.set_ylim(0, 60)
plt.title("sDCG (b=2, bq=4) with 10 queries")
plt.savefig('notes/figures/sdcg_10queries.pdf', bbox_inches='tight')
plt.show()
########################################################################################################################
########################################################################################################################
