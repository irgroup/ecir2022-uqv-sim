from repro_eval.Evaluator import RpdEvaluator
import os; os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64/"
from pyserini.search import SimpleSearcher, get_topics, get_qrels
from pyserini.index import IndexReader
import pytrec_eval
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats.stats import kendalltau

from utils import uqv, qcmcqg, trec, parse_results, sort_dict
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

qf = 0

data = {}

for user in tqdm(range(1, 9)):
    _data = {}

    run = {}
    for topic in topics.keys():
        query = list(df_uqv[(df_uqv['topic'] == topic) & (df_uqv['user'] == user)]['qstr'])[qf]
        results = searcher.search(q=query, k=k)
        run.update(parse_results(results, topic=str(topic)))

    rpd_eval.run_b_orig = run

    for sim in ['tts_s1', 'tts_s2', 'tts_s3', 'tts_s4', 'tts_s5', 'kis_s1', 'kis_s2', 'kis_s3', 'kis_s4', 'kis_s5',
                'qcmcqg_tts_s6', 'qcmcqg_tts_s7', 'qcmcqg_tts_s8', 'qcmcqg_kis_s6', 'qcmcqg_kis_s7', 'qcmcqg_kis_s8']:

        run = {}
        for topic in topics.keys():

            if sim == 'kis_s1':
                query = list(df_trec[(df_trec['strategy'] == 's1') & (df_trec['topic'] == topic)]['kis'])[qf]
            if sim == 'kis_s2':
                query = list(df_trec[(df_trec['strategy'] == 's2') & (df_trec['topic'] == topic)]['kis'])[qf]
            if sim == 'kis_s3':
                query = list(df_trec[(df_trec['strategy'] == 's3') & (df_trec['topic'] == topic)]['kis'])[qf]
            if sim == 'kis_s4':
                query = list(df_trec[(df_trec['strategy'] == 's4') & (df_trec['topic'] == topic)]['kis'])[qf]
            if sim == 'kis_s5':
                query = list(df_trec[(df_trec['strategy'] == 's5') & (df_trec['topic'] == topic)]['kis'])[qf]
            if sim == 'tts_s1':
                query = list(df_trec[(df_trec['strategy'] == 's1') & (df_trec['topic'] == topic)]['tts'])[qf]
            if sim == 'tts_s2':
                query = list(df_trec[(df_trec['strategy'] == 's2') & (df_trec['topic'] == topic)]['tts'])[qf]
            if sim == 'tts_s3':
                query = list(df_trec[(df_trec['strategy'] == 's3') & (df_trec['topic'] == topic)]['tts'])[qf]
            if sim == 'tts_s4':
                query = list(df_trec[(df_trec['strategy'] == 's4') & (df_trec['topic'] == topic)]['tts'])[qf]
            if sim == 'tts_s5':
                query = list(df_trec[(df_trec['strategy'] == 's5') & (df_trec['topic'] == topic)]['tts'])[qf]
            if sim == 'qcmcqg_kis_s6':
                query = list(df_qcmcqg[df_qcmcqg['topic'] == topic]['qcmcqg_kis_s6'])[qf]
            if sim == 'qcmcqg_kis_s7':
                query = list(df_qcmcqg[df_qcmcqg['topic'] == topic]['qcmcqg_kis_s7'])[qf]
            if sim == 'qcmcqg_kis_s8':
                query = list(df_qcmcqg[df_qcmcqg['topic'] == topic]['qcmcqg_kis_s8'])[qf]
            if sim == 'qcmcqg_tts_s6':
                query = list(df_qcmcqg[df_qcmcqg['topic'] == topic]['qcmcqg_tts_s6'])[qf]
            if sim == 'qcmcqg_tts_s7':
                query = list(df_qcmcqg[df_qcmcqg['topic'] == topic]['qcmcqg_tts_s7'])[qf]
            if sim == 'qcmcqg_tts_s8':
                query = list(df_qcmcqg[df_qcmcqg['topic'] == topic]['qcmcqg_tts_s8'])[qf]

            results = searcher.search(q=query, k=k)
            run.update(parse_results(results, topic=str(topic)))

        rpd_eval.run_b_rep = run
        rpd_eval.evaluate()
        _data[sim] = rpd_eval.ttest().get('baseline').get('ndcg')
    data[user] = _data

pd.DataFrame.from_dict(data).to_csv('data/experimental_results/ttest.csv')

########################################################################################################################
########################################################################################################################
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
file_in = 'data/experimental_results/ttest.csv'
df = pd.read_csv(file_in, index_col=0)

df = df.loc[['tts_s3', 'qcmcqg_tts_s6', 'qcmcqg_tts_s7', 'qcmcqg_tts_s8',
             'kis_s3', 'qcmcqg_kis_s6', 'qcmcqg_kis_s7', 'qcmcqg_kis_s8']]
df.index = ['$\mathregular{TTS_{S2}\prime}$', '$\mathregular{TTS_{S4}}$', '$\mathregular{TTS_{S4}\prime}$', '$\mathregular{TTS_{S4}\prime\prime}$',
            '$\mathregular{KIS_{S2}\prime}$', '$\mathregular{KIS_{S4}}$', '$\mathregular{KIS_{S4}\prime}$', '$\mathregular{KIS_{S4}\prime\prime}$']
fig, ax = plt.subplots(figsize=(12, 3))
for item in ax.get_yticklabels():
    item.set_fontsize(14)

ax = sns.heatmap(df, cmap=sns.color_palette("PuBu", as_cmap=True), linewidth=2, annot=True, fmt="0.4f")
ax.set_xlabel("UQV")
ax.set_ylabel('Simulator')
out_name = ''.join(['data/figures/ttest', '.pdf'])
plt.savefig(out_name, bbox_inches='tight')
plt.show()
########################################################################################################################
########################################################################################################################
