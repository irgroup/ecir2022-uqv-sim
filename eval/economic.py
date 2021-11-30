import os; os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64/"
from repro_eval.Evaluator import RpdEvaluator
from pyserini.search import SimpleSearcher, get_topics, get_qrels
import pandas as pd

USER = 5
trec_measure = 'ndcg'

searcher = SimpleSearcher(config['PATH_IDX'])
topics = get_topics('core17')
qrels = get_qrels('core17')

df_uqv = uqv()
df_trec = trec()
df_qcmcqg = qcmcqg()

rpd_eval = RpdEvaluator(qrel_orig_path=config['QREL'])

data = {}
ndcg_thresh = 0.5

k_list = list(range(1, 51, 1)) + list(range(50, 105, 5)) + list(range(100, 510, 10)) + list(range(500, 1050, 50)) + list(range(1000, 100100, 100))

for sim in ['uqv_5', 'tts_s3', 'kis_s3', 'qcmcqg_tts_s6', 'qcmcqg_tts_s7', 'qcmcqg_tts_s8']:
    _data = {}
    for q_max in range(1, 11):
        cnt = 0
        ndcg_tmp = 0.0
        while ndcg_tmp < ndcg_thresh:
            k = k_list[cnt]
            cnt += 1
            runs = {}
            for q in range(0, q_max):
                run = {}
                for topic in topics.keys():
                    if sim == 'uqv_5':
                        query = list(df_uqv[(df_uqv['topic'] == topic) & (df_uqv['user'] == USER)]['qstr'])[q]
                    if sim == 'kis_s3':
                        query = list(df_trec[(df_trec['strategy'] == 's3') & (df_trec['topic'] == topic)]['kis'])[q]
                    if sim == 'tts_s3':
                        query = list(df_trec[(df_trec['strategy'] == 's3') & (df_trec['topic'] == topic)]['tts'])[q]
                    if sim == 'qcmcqg_tts_s6':
                        query = list(df_qcmcqg[df_qcmcqg['topic'] == topic]['qcmcqg_tts_s6'])[q]
                    if sim == 'qcmcqg_tts_s7':
                        query = list(df_qcmcqg[df_qcmcqg['topic'] == topic]['qcmcqg_tts_s7'])[q]
                    if sim == 'qcmcqg_tts_s8':
                        query = list(df_qcmcqg[df_qcmcqg['topic'] == topic]['qcmcqg_tts_s8'])[q]
                    results = searcher.search(q=query, k=k)
                    run.update(parse_results(results, topic=str(topic)))
                runs[q] = run
            ndcg_tmp = 0.0
            for qf, run in runs.items():
                ndcg_tmp += sum([score.get(trec_measure) for topic, score in rpd_eval.rel_eval.evaluate(run).items()]) / len(topics)
        _data[q_max] = k
        print('simulator', sim)
        print('number of queries:', q_max, 'depth:', k)

    data[sim] = _data
pd.DataFrame.from_dict(data).to_csv(''.join(['economic', str(ndcg_thresh), '.csv']))

########################################################################################################################
########################################################################################################################
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')
ndcg_thresh = 0.3
in_name = ''.join(['data/experimental_results/economic', str(ndcg_thresh), '.csv'])
ax = pd.read_csv(in_name, index_col=0).plot(figsize=(4, 4), logy=True)
ax.legend(['$\mathregular{UQV_{5}}$', '$\mathregular{TTS_{S2}\prime}$', '$\mathregular{KIS_{S2}\prime}$',
           '$\mathregular{TTS_{S4}}$','$\mathregular{TTS_{S4}\prime}$', '$\mathregular{TTS_{S4}\prime\prime}$'],
           loc='upper right', fontsize=12)
ax.set_xlabel("Number of queries")
ax.set_ylabel('Depth')
plt.title("Number of queries vs. depth (nDCG " + str(ndcg_thresh) + ")")
out_name = ''.join(['data/figures/economic', str(ndcg_thresh), '.pdf'])
plt.savefig(out_name, bbox_inches='tight')
plt.show()

ndcg_thresh = 0.4
in_name = ''.join(['data/experimental_results/economic', str(ndcg_thresh), '.csv'])
ax = pd.read_csv(in_name, index_col=0).plot(figsize=(4, 4), logy=True)
ax.legend(['$\mathregular{UQV_{5}}$', '$\mathregular{TTS_{S2}\prime}$', '$\mathregular{KIS_{S2}\prime}$',
           '$\mathregular{TTS_{S4}}$','$\mathregular{TTS_{S4}\prime}$', '$\mathregular{TTS_{S4}\prime\prime}$'],
           loc='upper right', fontsize=12)
ax.set_xlabel("Number of queries")
ax.set_ylabel('Depth')
plt.title("Number of queries vs. depth (nDCG " + str(ndcg_thresh) + ")")
out_name = ''.join(['data/figures/economic', str(ndcg_thresh), '.pdf'])
plt.savefig(out_name, bbox_inches='tight')
plt.show()

ndcg_thresh = 0.5
in_name = ''.join(['data/experimental_results/economic', str(ndcg_thresh), '.csv'])
ax = pd.read_csv(in_name, index_col=0).plot(figsize=(4, 4), logy=True)
ax.legend(['$\mathregular{UQV_{5}}$', '$\mathregular{TTS_{S2}\prime}$', '$\mathregular{KIS_{S2}\prime}$',
           '$\mathregular{TTS_{S4}}$','$\mathregular{TTS_{S4}\prime}$', '$\mathregular{TTS_{S4}\prime\prime}$'],
           loc='upper right', fontsize=12)
ax.set_xlabel("Number of queries")
ax.set_ylabel('Depth')
plt.title("Number of queries vs. depth (nDCG " + str(ndcg_thresh) + ")")
out_name = ''.join(['data/figures/economic', str(ndcg_thresh), '.pdf'])
plt.savefig(out_name, bbox_inches='tight')
plt.show()
########################################################################################################################
########################################################################################################################