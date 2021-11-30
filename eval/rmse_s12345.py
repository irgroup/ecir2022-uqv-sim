import os; os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64/"
import seaborn as sns
from repro_eval.Evaluator import RpdEvaluator
from pyserini.search import SimpleSearcher, get_topics, get_qrels
import pandas as pd
import matplotlib.pyplot as plt
from config import default as config
from utils import parse_results

sns.set_style("darkgrid")

k = 100

searcher = SimpleSearcher(config['PATH_IDX'])
topics = get_topics('core17')
qrels = get_qrels('core17')

df_uqv = uqv()
df_trec = trec()

_rbo_tts = {}
_nrmse_tts = {}
_rbo_kis = {}
_nrmse_kis = {}


def get_result_list(queries, k):
    result_list = []
    docid_list = []
    for query in queries:
        pyserini_results = searcher.search(query, k=k)
        for result in pyserini_results:
            if result.docid not in docid_list:
                # if result.docid not in docid_list and result.docid in rel_docids:
                result_list.append(result)
                docid_list.append(result.docid)

    return result_list


for user in df_uqv['user'].unique():

    _rbo_tts[user] = {}
    _nrmse_tts[user] = {}
    _rbo_kis[user] = {}
    _nrmse_kis[user] = {}

    ### retrieval
    run = {}
    run_tts_s1 = {}
    run_tts_s2 = {}
    run_tts_s3 = {}
    run_tts_s4 = {}
    run_tts_s5 = {}
    run_kis_s1 = {}
    run_kis_s2 = {}
    run_kis_s3 = {}
    run_kis_s4 = {}
    run_kis_s5 = {}

    for topic in topics.keys():

        # q_tts_s1 = df_trec[(df_trec['strategy'] == 's1') & (df_trec['topic'] == topic)]['tts']
        # q_tts_s2 = df_trec[(df_trec['strategy'] == 's2') & (df_trec['topic'] == topic)]['tts']
        # q_tts_s3 = df_trec[(df_trec['strategy'] == 's3') & (df_trec['topic'] == topic)]['tts']
        # q_tts_s4 = df_trec[(df_trec['strategy'] == 's4') & (df_trec['topic'] == topic)]['tts']
        # q_tts_s5 = df_trec[(df_trec['strategy'] == 's5') & (df_trec['topic'] == topic)]['tts']
        # q_kis_s1 = df_trec[(df_trec['strategy'] == 's1') & (df_trec['topic'] == topic)]['kis']
        # q_kis_s2 = df_trec[(df_trec['strategy'] == 's2') & (df_trec['topic'] == topic)]['kis']
        # q_kis_s3 = df_trec[(df_trec['strategy'] == 's3') & (df_trec['topic'] == topic)]['kis']
        # q_kis_s4 = df_trec[(df_trec['strategy'] == 's4') & (df_trec['topic'] == topic)]['kis']
        # q_kis_s5 = df_trec[(df_trec['strategy'] == 's5') & (df_trec['topic'] == topic)]['kis']

        queries = df_uqv[(df_uqv['user'] == user) & (df_uqv['topic'] == topic)]['qstr']
        result_list = get_result_list(queries, k)
        run.update(parse_results(result_list, str(topic)))

        q_tts_s1 = list(df_trec[(df_trec['strategy'] == 's1') & (df_trec['topic'] == topic)]['tts'])[:len(queries)]
        result_list = get_result_list(q_tts_s1, k)
        run_tts_s1.update(parse_results(result_list, str(topic)))

        q_tts_s2 = list(df_trec[(df_trec['strategy'] == 's2') & (df_trec['topic'] == topic)]['tts'])[:len(queries)]
        result_list = get_result_list(q_tts_s2, k)
        run_tts_s2.update(parse_results(result_list, str(topic)))

        q_tts_s3 = list(df_trec[(df_trec['strategy'] == 's3') & (df_trec['topic'] == topic)]['tts'])[:len(queries)]
        result_list = get_result_list(q_tts_s3, k)
        run_tts_s3.update(parse_results(result_list, str(topic)))

        q_tts_s4 = list(df_trec[(df_trec['strategy'] == 's4') & (df_trec['topic'] == topic)]['tts'])[:len(queries)]
        result_list = get_result_list(q_tts_s4, k)
        run_tts_s4.update(parse_results(result_list, str(topic)))

        q_tts_s5 = list(df_trec[(df_trec['strategy'] == 's5') & (df_trec['topic'] == topic)]['tts'])[:len(queries)]
        result_list = get_result_list(q_tts_s5, k)
        run_tts_s5.update(parse_results(result_list, str(topic)))

        q_kis_s1 = list(df_trec[(df_trec['strategy'] == 's1') & (df_trec['topic'] == topic)]['kis'])[:len(queries)]
        result_list = get_result_list(q_kis_s1, k)
        run_kis_s1.update(parse_results(result_list, str(topic)))

        q_kis_s2 = list(df_trec[(df_trec['strategy'] == 's2') & (df_trec['topic'] == topic)]['kis'])[:len(queries)]
        result_list = get_result_list(q_kis_s2, k)
        run_kis_s2.update(parse_results(result_list, str(topic)))

        q_kis_s3 = list(df_trec[(df_trec['strategy'] == 's3') & (df_trec['topic'] == topic)]['kis'])[:len(queries)]
        result_list = get_result_list(q_kis_s3, k)
        run_kis_s3.update(parse_results(result_list, str(topic)))

        q_kis_s4 = list(df_trec[(df_trec['strategy'] == 's4') & (df_trec['topic'] == topic)]['kis'])[:len(queries)]
        result_list = get_result_list(q_kis_s4, k)
        run_kis_s4.update(parse_results(result_list, str(topic)))

        q_kis_s5 = list(df_trec[(df_trec['strategy'] == 's5') & (df_trec['topic'] == topic)]['kis'])[:len(queries)]
        result_list = get_result_list(q_kis_s5, k)
        run_kis_s5.update(parse_results(result_list, str(topic)))

    ### evaluation
    rpd_eval = RpdEvaluator(qrel_orig_path='data/qrels/core17.txt')
    rpd_eval.run_b_orig = run

    ### tts_s1
    rpd_eval.run_b_rep = run_tts_s1
    rpd_eval.evaluate()
    _nrmse_tts[user]['s1'] = rpd_eval.nrmse().get('baseline').get('ndcg')

    ### tts_s2
    rpd_eval.run_b_rep = run_tts_s2
    rpd_eval.evaluate()
    _nrmse_tts[user]['s2'] = rpd_eval.nrmse().get('baseline').get('ndcg')

    ### tts_s3
    rpd_eval.run_b_rep = run_tts_s3
    rpd_eval.evaluate()
    _nrmse_tts[user]['s3'] = rpd_eval.nrmse().get('baseline').get('ndcg')

    ### tts_s4
    rpd_eval.run_b_rep = run_tts_s4
    rpd_eval.evaluate()
    _nrmse_tts[user]['s4'] = rpd_eval.nrmse().get('baseline').get('ndcg')

    ### tts_s5
    rpd_eval.run_b_rep = run_tts_s5
    rpd_eval.evaluate()
    _nrmse_tts[user]['s5'] = rpd_eval.nrmse().get('baseline').get('ndcg')

    ### kis_s1
    rpd_eval.run_b_rep = run_kis_s1
    rpd_eval.evaluate()
    _nrmse_kis[user]['s1'] = rpd_eval.nrmse().get('baseline').get('ndcg')

    ### kis_s2
    rpd_eval.run_b_rep = run_kis_s2
    rpd_eval.evaluate()
    _nrmse_kis[user]['s2'] = rpd_eval.nrmse().get('baseline').get('ndcg')

    ### kis_s3
    rpd_eval.run_b_rep = run_kis_s3
    rpd_eval.evaluate()
    _nrmse_kis[user]['s3'] = rpd_eval.nrmse().get('baseline').get('ndcg')

    ### kis_s4
    rpd_eval.run_b_rep = run_kis_s4
    rpd_eval.evaluate()
    _nrmse_kis[user]['s4'] = rpd_eval.nrmse().get('baseline').get('ndcg')

    ### kis_s5
    rpd_eval.run_b_rep = run_kis_s5
    rpd_eval.evaluate()
    _nrmse_kis[user]['s5'] = rpd_eval.nrmse().get('baseline').get('ndcg')


df = pd.DataFrame.from_dict(_nrmse_tts).transpose()
df.to_csv('data/experimental_results/rmse_uqv_vs_s12345_tts_ndcg.csv')
ax = df.plot.bar()
ax.set_xlabel("User")
ax.set_ylabel("nRMSE (nDCG)")
ax.legend(['S1', 'S2', 'S3', 'S4', 'S5'])
plt.legend(title='Strategy')
plt.title('UQV vs. TTS')
plt.show()

df = pd.DataFrame.from_dict(_nrmse_kis).transpose()
df.to_csv('data/experimental_results/rmse_uqv_vs_s12345_kis_ndcg.csv')
ax = df.plot.bar()
ax.set_xlabel("User")
ax.set_ylabel("nRMSE (nDCG)")
ax.legend(['S1', 'S2', 'S3', 'S4', 'S5'])
plt.legend(title='Strategy')
plt.title('UQV vs. KIS')
plt.show()

########################################################################################################################
########################################################################################################################
df = pd.read_csv('data/experimental_results/rmse_uqv_vs_s12345_tts_ndcg.csv', index_col=0)
ax = df.plot.bar(figsize=(6,3))
ax.set_ylim(0.0, 0.525)
ax.set_xlabel("UQV")
ax.set_ylabel("RMSE (nDCG)")
plt.legend(labels=['S1', 'S2', 'S$\mathregular{2\prime}$', 'S3', 'S$\mathregular{3\prime}$'], loc='lower right')
plt.title('UQV vs. TTS')
plt.savefig('data/figures/rmse_uqv_vs_s12345_tts_ndcg.pdf', bbox_inches='tight')
plt.show()

df = pd.read_csv('data/experimental_results/rmse_uqv_vs_s12345_kis_ndcg.csv', index_col=0)
ax = df.plot.bar(figsize=(6,3))
ax.set_ylim(0.0, 0.525)
ax.set_xlabel("UQV")
ax.set_ylabel("RMSE (nDCG)")
plt.legend(labels=['S1', 'S2', 'S$\mathregular{2\prime}$', 'S3', 'S$\mathregular{3\prime}$'], loc='lower right')
plt.title('UQV vs. KIS')
plt.savefig('data/figures/rmse_uqv_vs_s12345_kis_ndcg.pdf', bbox_inches='tight')
plt.show()
########################################################################################################################
########################################################################################################################
