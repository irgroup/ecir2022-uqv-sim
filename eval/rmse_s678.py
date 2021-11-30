from repro_eval.Evaluator import RpdEvaluator
import os; os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64/"
from pyserini.search import SimpleSearcher, get_topics, get_qrels
import pytrec_eval
import pandas as pd

from utils import uqv, qcmcqg, trec, parse_results
from config import default as config

USER = 5
_q = 10
strategy = 's3'
trec_measure = 'P_1000'

searcher = SimpleSearcher(config['PATH_IDX'])
topics = get_topics('core17')
qrels = get_qrels('core17')


def cumulative_rel_docs(qs, k, q):
    run = {}
    # length = 0
    for topic in topics:

        rel_docids = [str(docid) for docid, qrel in qrels.get(topic).items() if int(qrel) > 0]

        # qstrs = list(df_trec[(df_trec['topic'] == topic) & (df_trec['strategy'] == 's3')]['kis'])
        # qstrs = list(df_uqv[(df_uqv['topic'] == topic) & (df_uqv['user'] == USER)]['qstr'])

        qstrs = qs.get(topic)

        result_list = []
        docid_list = []
        for qstr in qstrs[:q]:
            pyserini_results = searcher.search(qstr, k=k)
            for result in pyserini_results:
                if result.docid not in docid_list:
                # if result.docid not in docid_list and result.docid in rel_docids:
                    result_list.append(result)
                    docid_list.append(result.docid)
                # result_list.append(result)
        # length += len(result_list)
        run.update(parse_results(result_list, str(topic)))
    # print(length)
    return run


with open(config['QREL'], 'r') as f_qrel:
    qrel_orig = pytrec_eval.parse_qrel(f_qrel)
    rel_eval = pytrec_eval.RelevanceEvaluator(qrel_orig, pytrec_eval.supported_measures)

df_uqv = uqv()
df_trec = trec()
df_qcmcqg = qcmcqg()


_data = {'kis':{},
         'tts':{},
         'qcmcqg_tts_s6': {},
         'qcmcqg_tts_s7': {},
         'qcmcqg_tts_s8': {}}


for _k in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
    print('k=', _k, 'q=', _q, trec_measure, USER)

    qs = {topic: list(df_uqv[(df_uqv['topic'] == topic) & (df_uqv['user'] == USER)]['qstr']) for topic in topics}
    run = cumulative_rel_docs(qs=qs, k=_k, q=_q)
    evals = rel_eval.evaluate(run)

    rpd_eval = RpdEvaluator(qrel_orig_path='data/qrels/core17.txt')
    rpd_eval.run_b_orig = run


    qs = {topic: list(df_trec[(df_trec['topic'] == topic) & (df_trec['strategy'] == strategy)]['kis']) for topic in topics}
    run = cumulative_rel_docs(qs=qs, k=_k, q=_q)
    rpd_eval.run_b_rep = run
    rpd_eval.evaluate()
    print('kis:', rpd_eval.nrmse().get('baseline').get(trec_measure))
    _data['kis'][_k] = rpd_eval.nrmse().get('baseline').get(trec_measure)

    qs = {topic: list(df_trec[(df_trec['topic'] == topic) & (df_trec['strategy'] == strategy)]['tts']) for topic in topics}
    run = cumulative_rel_docs(qs=qs, k=_k, q=_q)
    rpd_eval.run_b_rep = run
    rpd_eval.evaluate()
    print('tts:', rpd_eval.nrmse().get('baseline').get(trec_measure))
    _data['tts'][_k] = rpd_eval.nrmse().get('baseline').get(trec_measure)

    qs = {topic: list(df_qcmcqg[df_qcmcqg['topic'] == topic]['qcmcqg_tts_s6']) for topic in topics}
    run = cumulative_rel_docs(qs=qs, k=_k, q=_q)
    rpd_eval.run_b_rep = run
    rpd_eval.evaluate()
    print('qcmcqg_tts_s6:', rpd_eval.nrmse().get('baseline').get(trec_measure))
    _data['qcmcqg_tts_s6'][_k] = rpd_eval.nrmse().get('baseline').get(trec_measure)

    qs = {topic: list(df_qcmcqg[df_qcmcqg['topic'] == topic]['qcmcqg_tts_s7']) for topic in topics}
    run = cumulative_rel_docs(qs=qs, k=_k, q=_q)
    rpd_eval.run_b_rep = run
    rpd_eval.evaluate()
    print('qcmcqg_tts_s7:', rpd_eval.nrmse().get('baseline').get(trec_measure))
    _data['qcmcqg_tts_s7'][_k] = rpd_eval.nrmse().get('baseline').get(trec_measure)

    qs = {topic: list(df_qcmcqg[df_qcmcqg['topic'] == topic]['qcmcqg_tts_s8']) for topic in topics}
    run = cumulative_rel_docs(qs=qs, k=_k, q=_q)
    rpd_eval.run_b_rep = run
    rpd_eval.evaluate()
    print('qcmcqg_tts_s8:', rpd_eval.nrmse().get('baseline').get(trec_measure))
    _data['qcmcqg_tts_s8'][_k] = rpd_eval.nrmse().get('baseline').get(trec_measure)

# pd.DataFrame.from_dict(_data).to_csv('data/experimental_results/rmse_map.csv')
# pd.DataFrame.from_dict(_data).to_csv('data/experimental_results/rmse_ndcg.csv')
pd.DataFrame.from_dict(_data).to_csv('data/experimental_results/rmse_p1000.csv')

########################################################################################################################
########################################################################################################################
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')

_fs = (4, 4)

df = pd.read_csv('data/experimental_results/rmse_map.csv', index_col=0)
ax = df.plot(figsize=_fs)
ax.legend(['$\mathregular{TTS_{S2}\prime}$', '$\mathregular{KIS_{S2}\prime}$',
           '$\mathregular{TTS_{S4}}$','$\mathregular{TTS_{S4}\prime}$',
           '$\mathregular{TTS_{S4}\prime\prime}$'],
           loc='lower right', fontsize=12)
ax.set_xlabel("Number of documents per query")
ax.set_ylabel("RMSE (AP)")
plt.title('RMSE (AP) between \n $\mathregular{UQV_{5}}$ and query simulations')
# plt.title('nRMSE (AP)')
plt.savefig('data/figures/rmse_map.pdf', bbox_inches='tight')
plt.show()
########################################################################################################################
########################################################################################################################
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')

df = pd.read_csv('data/experimental_results/rmse_p1000.csv', index_col=0)
ax = df.plot(figsize=_fs)
ax.legend(['$\mathregular{TTS_{S2}\prime}$', '$\mathregular{KIS_{S2}\prime}$',
           '$\mathregular{TTS_{S4}}$','$\mathregular{TTS_{S4}\prime}$',
           '$\mathregular{TTS_{S4}\prime\prime}$'],
           loc='lower right', fontsize=12)
ax.set_xlabel("Number of documents per query")
ax.set_ylabel("RMSE (P@1000)")
plt.title('RMSE (P@1000) between \n $\mathregular{UQV_{5}}$ and query simulations')
plt.savefig('data/figures/rmse_p1000.pdf', bbox_inches='tight')
plt.show()
########################################################################################################################
########################################################################################################################
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')

df = pd.read_csv('data/experimental_results/rmse_ndcg.csv', index_col=0)
ax = df.plot(figsize=_fs)
ax.legend(['$\mathregular{TTS_{S2}\prime}$', '$\mathregular{KIS_{S2}\prime}$',
           '$\mathregular{TTS_{S4}}$','$\mathregular{TTS_{S4}\prime}$',
           '$\mathregular{TTS_{S4}\prime\prime}$'],
           loc='lower right', fontsize=12)
ax.set_xlabel("Number of documents per query")
ax.set_ylabel("RMSE (nDCG)")
plt.title('RMSE (nDCG) between \n $\mathregular{UQV_{5}}$ and query simulations')
plt.savefig('data/figures/rmse_ndcg.pdf', bbox_inches='tight')
plt.show()
########################################################################################################################
########################################################################################################################
