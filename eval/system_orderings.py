from repro_eval.Evaluator import RpdEvaluator
import os; os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64/"
from pyserini.search import SimpleSearcher, get_topics, get_qrels
import pandas as pd
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

# sys_configs = ['bm25_rm3_default',
#                'qld_rm3_default',
#                'qld_rm3_fbt5_fbd5',
#                'qld_rm3_fbt3_fbd2',
#                'bm25_default',
#                'qld_100',
#                'bm25_b_0.0',
#                'qld_mu_10',
#                'bm25_k1_10.0_b_0.0',
#                'bm25_k1_15.0_b_0.0',
#                'bm25_k1_20.0_b_0.0',
#                'bm25_k1_30.0_b_0.0',
#                'bm25_k1_50.0_b_0.0',
#                'bm25_k1_100.0_b_0.0',
#                'bm25_k1_500.0_b_0.0',
#                'bm25_k1_0.0_b_0.0']

data = {'tts_s1': {},
        'tts_s2': {},
        'tts_s3': {},
        'tts_s4': {},
        'tts_s5': {},
        'kis_s1': {},
        'kis_s2': {},
        'kis_s3': {},
        'kis_s4': {},
        'kis_s5': {},
        'qcmcqg_kis_s6': {},
        'qcmcqg_kis_s7': {},
        'qcmcqg_kis_s8': {},
        'qcmcqg_tts_s6': {},
        'qcmcqg_tts_s7': {},
        'qcmcqg_tts_s8': {}}

sys_configs = ['qld_mu_50',
               'qld_mu_250',
               'qld_mu_500',
               'qld_mu_1250',
               'qld_mu_2500',
               'qld_mu_5000']

for qf in tqdm(range(0, 10)):
    sys_rank_user = {}
    sys_rank_sim_tts_s1 = {}
    sys_rank_sim_tts_s2 = {}
    sys_rank_sim_tts_s3 = {}
    sys_rank_sim_tts_s4 = {}
    sys_rank_sim_tts_s5 = {}
    sys_rank_sim_kis_s1 = {}
    sys_rank_sim_kis_s2 = {}
    sys_rank_sim_kis_s3 = {}
    sys_rank_sim_kis_s4 = {}
    sys_rank_sim_kis_s5 = {}
    sys_rank_sim_qcmcqg_tts_s6 = {}
    sys_rank_sim_qcmcqg_tts_s7 = {}
    sys_rank_sim_qcmcqg_tts_s8 = {}
    sys_rank_sim_qcmcqg_kis_s6 = {}
    sys_rank_sim_qcmcqg_kis_s7 = {}
    sys_rank_sim_qcmcqg_kis_s8 = {}

    for sys_config in sys_configs:

        if sys_config == 'bm25_rm3_default':
            searcher.set_rm3()
        if sys_config == 'qld_rm3_default':
            searcher.set_qld()
            searcher.set_rm3()
        if sys_config == 'qld_rm3_fbt5_fbd5':
            searcher.set_qld()
            searcher.set_rm3(fb_terms=5, fb_docs=5)
        if sys_config == 'qld_rm3_fbt3_fbd2':
            searcher.set_qld()
            searcher.set_rm3(fb_terms=3, fb_docs=2)
        if sys_config == 'bm25_default':
            searcher.set_bm25()
        if sys_config == 'qld_100':
            searcher.set_qld(mu=100)
        if sys_config == 'bm25_b_0.0':
            searcher.set_bm25(b=0.0)
        if sys_config == 'qld_mu_10':
            searcher.set_qld(mu=10)
        if sys_config == 'bm25_k1_10.0_b_0.0':
            searcher.set_bm25(k1=10.0, b=0.0)
        if sys_config == 'bm25_k1_15.0_b_0.0':
            searcher.set_bm25(k1=15.0, b=0.0)
        if sys_config == 'bm25_k1_20.0_b_0.0':
            searcher.set_bm25(k1=20.0, b=0.0)
        if sys_config == 'bm25_k1_30.0_b_0.0':
            searcher.set_bm25(k1=30.0, b=0.0)
        if sys_config == 'bm25_k1_50.0_b_0.0':
            searcher.set_bm25(k1=50.0, b=0.0)
        if sys_config == 'bm25_k1_100.0_b_0.0':
            searcher.set_bm25(k1=100.0, b=0.0)
        if sys_config == 'bm25_k1_500.0_b_0.0':
            searcher.set_bm25(k1=500.0, b=0.0)
        if sys_config == 'bm25_k1_0.0_b_0.0':
            searcher.set_bm25(k1=0.0, b=0.0)

        if sys_config == 'qld_mu_50':
            searcher.set_qld(mu=50)
        if sys_config == 'qld_mu_250':
            searcher.set_qld(mu=250)
        if sys_config == 'qld_mu_500':
            searcher.set_qld(mu=500)
        if sys_config == 'qld_mu_1250':
            searcher.set_qld(mu=1250)
        if sys_config == 'qld_mu_2500':
            searcher.set_qld(mu=2500)
        if sys_config == 'qld_mu_5000':
            searcher.set_qld(mu=5000)

        run_user = {}
        for topic in topics.keys():
            query_user = list(df_uqv[(df_uqv['topic'] == topic) & (df_uqv['user'] == USER)]['qstr'])[qf]
            results = searcher.search(q=query_user, k=k)
            run_user.update(parse_results(results, topic=str(topic)))
        sys_rank_user[sys_config] = sum([score.get(trec_measure) for topic, score in rpd_eval.rel_eval.evaluate(run_user).items()]) / len(topics)

        run_sim = {}
        for topic in topics.keys():
            query_sim = list(df_trec[(df_trec['topic'] == topic) & (df_trec['strategy'] == 's1')]['tts'])[qf]
            results = searcher.search(q=query_sim, k=k)
            run_sim.update(parse_results(results, topic=str(topic)))
        sys_rank_sim_tts_s1[sys_config] = sum([score.get(trec_measure) for topic, score in rpd_eval.rel_eval.evaluate(run_sim).items()]) / len(topics)

        run_sim = {}
        for topic in topics.keys():
            query_sim = list(df_trec[(df_trec['topic'] == topic) & (df_trec['strategy'] == 's2')]['tts'])[qf]
            results = searcher.search(q=query_sim, k=k)
            run_sim.update(parse_results(results, topic=str(topic)))
        sys_rank_sim_tts_s2[sys_config] = sum([score.get(trec_measure) for topic, score in rpd_eval.rel_eval.evaluate(run_sim).items()]) / len(topics)

        run_sim = {}
        for topic in topics.keys():
            query_sim = list(df_trec[(df_trec['topic'] == topic) & (df_trec['strategy'] == 's3')]['tts'])[qf]
            results = searcher.search(q=query_sim, k=k)
            run_sim.update(parse_results(results, topic=str(topic)))
        sys_rank_sim_tts_s3[sys_config] = sum([score.get(trec_measure) for topic, score in rpd_eval.rel_eval.evaluate(run_sim).items()]) / len(topics)

        run_sim = {}
        for topic in topics.keys():
            query_sim = list(df_trec[(df_trec['topic'] == topic) & (df_trec['strategy'] == 's4')]['tts'])[qf]
            results = searcher.search(q=query_sim, k=k)
            run_sim.update(parse_results(results, topic=str(topic)))
        sys_rank_sim_tts_s4[sys_config] = sum([score.get(trec_measure) for topic, score in rpd_eval.rel_eval.evaluate(run_sim).items()]) / len(topics)

        run_sim = {}
        for topic in topics.keys():
            query_sim = list(df_trec[(df_trec['topic'] == topic) & (df_trec['strategy'] == 's5')]['tts'])[qf]
            results = searcher.search(q=query_sim, k=k)
            run_sim.update(parse_results(results, topic=str(topic)))
        sys_rank_sim_tts_s5[sys_config] = sum([score.get(trec_measure) for topic, score in rpd_eval.rel_eval.evaluate(run_sim).items()]) / len(topics)

        ### trec kis

        run_sim = {}
        for topic in topics.keys():
            query_sim = list(df_trec[(df_trec['topic'] == topic) & (df_trec['strategy'] == 's1')]['kis'])[qf]
            results = searcher.search(q=query_sim, k=k)
            run_sim.update(parse_results(results, topic=str(topic)))
        sys_rank_sim_kis_s1[sys_config] = sum([score.get(trec_measure) for topic, score in rpd_eval.rel_eval.evaluate(run_sim).items()]) / len(topics)

        run_sim = {}
        for topic in topics.keys():
            query_sim = list(df_trec[(df_trec['topic'] == topic) & (df_trec['strategy'] == 's2')]['kis'])[qf]
            results = searcher.search(q=query_sim, k=k)
            run_sim.update(parse_results(results, topic=str(topic)))
        sys_rank_sim_kis_s2[sys_config] = sum([score.get(trec_measure) for topic, score in rpd_eval.rel_eval.evaluate(run_sim).items()]) / len(topics)

        run_sim = {}
        for topic in topics.keys():
            query_sim = list(df_trec[(df_trec['topic'] == topic) & (df_trec['strategy'] == 's3')]['kis'])[qf]
            results = searcher.search(q=query_sim, k=k)
            run_sim.update(parse_results(results, topic=str(topic)))
        sys_rank_sim_kis_s3[sys_config] = sum([score.get(trec_measure) for topic, score in rpd_eval.rel_eval.evaluate(run_sim).items()]) / len(topics)

        run_sim = {}
        for topic in topics.keys():
            query_sim = list(df_trec[(df_trec['topic'] == topic) & (df_trec['strategy'] == 's4')]['kis'])[qf]
            results = searcher.search(q=query_sim, k=k)
            run_sim.update(parse_results(results, topic=str(topic)))
        sys_rank_sim_kis_s4[sys_config] = sum([score.get(trec_measure) for topic, score in rpd_eval.rel_eval.evaluate(run_sim).items()]) / len(topics)

        run_sim = {}
        for topic in topics.keys():
            query_sim = list(df_trec[(df_trec['topic'] == topic) & (df_trec['strategy'] == 's5')]['kis'])[qf]
            results = searcher.search(q=query_sim, k=k)
            run_sim.update(parse_results(results, topic=str(topic)))
        sys_rank_sim_kis_s5[sys_config] = sum([score.get(trec_measure) for topic, score in rpd_eval.rel_eval.evaluate(run_sim).items()]) / len(topics)

        ### qcmcqg
        run_sim = {}
        for topic in topics.keys():
            query_sim = list(df_qcmcqg[df_qcmcqg['topic'] == topic]['qcmcqg_tts_s6'])[qf]
            results = searcher.search(q=query_sim, k=k)
            run_sim.update(parse_results(results, topic=str(topic)))
        sys_rank_sim_qcmcqg_tts_s6[sys_config] = sum([score.get(trec_measure) for topic, score in rpd_eval.rel_eval.evaluate(run_sim).items()]) / len(topics)

        run_sim = {}
        for topic in topics.keys():
            query_sim = list(df_qcmcqg[df_qcmcqg['topic'] == topic]['qcmcqg_tts_s7'])[qf]
            results = searcher.search(q=query_sim, k=k)
            run_sim.update(parse_results(results, topic=str(topic)))
        sys_rank_sim_qcmcqg_tts_s7[sys_config] = sum([score.get(trec_measure) for topic, score in rpd_eval.rel_eval.evaluate(run_sim).items()]) / len(topics)

        run_sim = {}
        for topic in topics.keys():
            query_sim = list(df_qcmcqg[df_qcmcqg['topic'] == topic]['qcmcqg_tts_s8'])[qf]
            results = searcher.search(q=query_sim, k=k)
            run_sim.update(parse_results(results, topic=str(topic)))
        sys_rank_sim_qcmcqg_tts_s8[sys_config] = sum([score.get(trec_measure) for topic, score in rpd_eval.rel_eval.evaluate(run_sim).items()]) / len(topics)

        run_sim = {}
        for topic in topics.keys():
            query_sim = list(df_qcmcqg[df_qcmcqg['topic'] == topic]['qcmcqg_kis_s6'])[qf]
            results = searcher.search(q=query_sim, k=k)
            run_sim.update(parse_results(results, topic=str(topic)))
        sys_rank_sim_qcmcqg_kis_s6[sys_config] = sum([score.get(trec_measure) for topic, score in rpd_eval.rel_eval.evaluate(run_sim).items()]) / len(topics)

        run_sim = {}
        for topic in topics.keys():
            query_sim = list(df_qcmcqg[df_qcmcqg['topic'] == topic]['qcmcqg_kis_s7'])[qf]
            results = searcher.search(q=query_sim, k=k)
            run_sim.update(parse_results(results, topic=str(topic)))
        sys_rank_sim_qcmcqg_kis_s7[sys_config] = sum([score.get(trec_measure) for topic, score in rpd_eval.rel_eval.evaluate(run_sim).items()]) / len(topics)

        run_sim = {}
        for topic in topics.keys():
            query_sim = list(df_qcmcqg[df_qcmcqg['topic'] == topic]['qcmcqg_kis_s8'])[qf]
            results = searcher.search(q=query_sim, k=k)
            run_sim.update(parse_results(results, topic=str(topic)))
        sys_rank_sim_qcmcqg_kis_s8[sys_config] = sum([score.get(trec_measure) for topic, score in rpd_eval.rel_eval.evaluate(run_sim).items()]) / len(topics)


        searcher.unset_rm3()
        searcher.set_bm25()

    sys_rank_user = sort_dict(sys_rank_user)
    sys_rank_sim_tts_s1 = sort_dict(sys_rank_sim_tts_s1)
    sys_rank_sim_tts_s2 = sort_dict(sys_rank_sim_tts_s2)
    sys_rank_sim_tts_s3 = sort_dict(sys_rank_sim_tts_s3)
    sys_rank_sim_tts_s4 = sort_dict(sys_rank_sim_tts_s4)
    sys_rank_sim_tts_s5 = sort_dict(sys_rank_sim_tts_s5)
    sys_rank_sim_kis_s1 = sort_dict(sys_rank_sim_kis_s1)
    sys_rank_sim_kis_s2 = sort_dict(sys_rank_sim_kis_s2)
    sys_rank_sim_kis_s3 = sort_dict(sys_rank_sim_kis_s3)
    sys_rank_sim_kis_s4 = sort_dict(sys_rank_sim_kis_s4)
    sys_rank_sim_kis_s5 = sort_dict(sys_rank_sim_kis_s5)
    sys_rank_sim_qcmcqg_tts_s6 = sort_dict(sys_rank_sim_qcmcqg_tts_s6)
    sys_rank_sim_qcmcqg_tts_s7 = sort_dict(sys_rank_sim_qcmcqg_tts_s7)
    sys_rank_sim_qcmcqg_tts_s8 = sort_dict(sys_rank_sim_qcmcqg_tts_s8)
    sys_rank_sim_qcmcqg_kis_s6 = sort_dict(sys_rank_sim_qcmcqg_kis_s6)
    sys_rank_sim_qcmcqg_kis_s7 = sort_dict(sys_rank_sim_qcmcqg_kis_s7)
    sys_rank_sim_qcmcqg_kis_s8 = sort_dict(sys_rank_sim_qcmcqg_kis_s8)

    data['tts_s1'][str(qf+1)] = kendalltau(list(sys_rank_user.keys()), list(sys_rank_sim_tts_s1.keys())).correlation
    data['tts_s2'][str(qf+1)] = kendalltau(list(sys_rank_user.keys()), list(sys_rank_sim_tts_s2.keys())).correlation
    data['tts_s3'][str(qf+1)] = kendalltau(list(sys_rank_user.keys()), list(sys_rank_sim_tts_s3.keys())).correlation
    data['tts_s4'][str(qf+1)] = kendalltau(list(sys_rank_user.keys()), list(sys_rank_sim_tts_s4.keys())).correlation
    data['tts_s5'][str(qf+1)] = kendalltau(list(sys_rank_user.keys()), list(sys_rank_sim_tts_s5.keys())).correlation
    data['kis_s1'][str(qf+1)] = kendalltau(list(sys_rank_user.keys()), list(sys_rank_sim_kis_s1.keys())).correlation
    data['kis_s2'][str(qf+1)] = kendalltau(list(sys_rank_user.keys()), list(sys_rank_sim_kis_s2.keys())).correlation
    data['kis_s3'][str(qf+1)] = kendalltau(list(sys_rank_user.keys()), list(sys_rank_sim_kis_s3.keys())).correlation
    data['kis_s4'][str(qf+1)] = kendalltau(list(sys_rank_user.keys()), list(sys_rank_sim_kis_s4.keys())).correlation
    data['kis_s5'][str(qf+1)] = kendalltau(list(sys_rank_user.keys()), list(sys_rank_sim_kis_s5.keys())).correlation
    data['qcmcqg_tts_s6'][str(qf+1)] = kendalltau(list(sys_rank_user.keys()), list(sys_rank_sim_qcmcqg_tts_s6.keys())).correlation
    data['qcmcqg_tts_s7'][str(qf+1)] = kendalltau(list(sys_rank_user.keys()), list(sys_rank_sim_qcmcqg_tts_s7.keys())).correlation
    data['qcmcqg_tts_s8'][str(qf+1)] = kendalltau(list(sys_rank_user.keys()), list(sys_rank_sim_qcmcqg_tts_s8.keys())).correlation
    data['qcmcqg_kis_s6'][str(qf+1)] = kendalltau(list(sys_rank_user.keys()), list(sys_rank_sim_qcmcqg_kis_s6.keys())).correlation
    data['qcmcqg_kis_s7'][str(qf+1)] = kendalltau(list(sys_rank_user.keys()), list(sys_rank_sim_qcmcqg_kis_s7.keys())).correlation
    data['qcmcqg_kis_s8'][str(qf+1)] = kendalltau(list(sys_rank_user.keys()), list(sys_rank_sim_qcmcqg_kis_s8.keys())).correlation

pd.DataFrame.from_dict(data).to_csv('data/experimental_results/system_orderings.csv')

########################################################################################################################
########################################################################################################################
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
df = pd.read_csv('data/experimental_results/kendalls_tau_system_orderings_user_5.csv', index_col=0)
df = df[['tts_s3', 'kis_s3', 'qcmcqg_tts_s6', 'qcmcqg_tts_s7', 'qcmcqg_tts_s8']]
df.columns = ['$\mathregular{TTS_{S2}\prime}$', '$\mathregular{KIS_{S2}\prime}$', '$\mathregular{TTS_{S4}}$', '$\mathregular{TTS_{S4}\prime}$', '$\mathregular{TTS_{S4}\prime\prime}$']
ax = sns.heatmap(df, cmap=sns.color_palette("RdBu", as_cmap=True), linewidth=2, annot=True, fmt="0.4f", center=0)
ax.set_xlabel("Query simulator")
ax.set_ylabel("Query formulation $q_i$")
plt.title("Kendall's " + r'$\tau$ ' + 'between system orderings')
plt.savefig('data/figures/system_orderings.pdf', bbox_inches='tight')
plt.show()
plt.show()
########################################################################################################################
########################################################################################################################
