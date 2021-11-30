# Validating Simulations of User Query Variants

This repository accompanies our submission to ECIR22. It contains the scripts of the experiments and evaluations, simulated queries, as well as the figures of the paper.

### Abstract:
>  System-oriented IR evaluations are limited to rather abstract understandings of real user behavior. As a solution, simulating user interactions provides a cost-efficient way to support system-oriented experiments with more realistic directives when no interaction logs are available. While there are several user models for simulated clicks or result list interactions, very few attempts have been made towards query simulations, and it has not been investigated if these can reproduce properties of real queries. In this work, we validate simulated user query variants with the help of TREC test collections in reference to real user queries that were made for the corresponding topics. Besides, we introduce a simple yet effective method that gives better reproductions of real queries than the established methods. Our evaluation framework validates the simulations regarding the retrieval performance, reproducibility of topic score distributions, shared task utility, effort and effect, and query term similarity when compared with real user query variants. While the retrieval effectiveness and statistical properties of the topic score distributions as well as economic aspects are close to that of real queries, it is still challenging to simulate exact term matches and later query reformulations.

### Directory overview

| Directory | Description | 
| --- | --- |
| `config/` | Contains configuration files for the query simulations, experiments, and evaluations. | 
| `data/` | Contains (intermediate) output data of the simulations and experiments as well as the figures of the paper. | 
| `eval/` | Contains scripts of the experiments and evaluations. | 
| `sim/` | Contains scripts of the query simulations. |

### Setup
1. Install [Anserini](https://github.com/castorini/anserini) and index [Core17 (The New York Times Annotated Corpus)](https://catalog.ldc.upenn.edu/LDC2008T19) according to the [regression guide](https://github.com/castorini/anserini/blob/master/docs/regressions-core17.md):
```
anserini/target/appassembler/bin/IndexCollection \
    -collection NewYorkTimesCollection \
    -input /path/to/core17/ \
    -index anserini/indexes/lucene-index.core17 \
    -generator DefaultLuceneDocumentGenerator \
    -threads 4 \
    -storePositions \
    -storeDocvectors \
    -storeRaw \
    -storeContents \
    > anserini/logs/log.core17 &
```

2. Install the required Python packages:
```
pip install -r requirements.txt
```

### Query simulation

In order to prepare the language models and simulate the queries, the scripts have to executed in the order shown in the following table. All of the outputs can be found in the `data/` directory. For the sake of better code readability the names of the query reformulation strategies have been mapped: 
`S1`  &rarr; `S1`; `S2`  &rarr; `S2`; `S2'`  &rarr; `S3`; `S3`  &rarr; `S4`; `S3'`  &rarr; `S5`; `S4`  &rarr; `S6`; `S4'`  &rarr; `S7`; `S4''`  &rarr; `S8`. The names of the scripts and output files comply with this name mapping.

| Script | Description | Output files | 
| --- | --- | --- |
| `sim/make_background.py` | Make the background language model form all index terms of Core17. The background model is required for Controlled Query Generation (CQG) by Jordan et al. | `data/lm/background.csv` | 
| `sim/make_cqg.py` | Make the CQG language models with different parameters of lambda from 0.0 to 1.0. | `data/lm/cqg.json` |
| `sim/simulate_queries_s12345.py` | Simulate TTS and KIS queries with strategies S1 to S3' | `data/queries/s12345.csv` |
| `sim/simulate_queries_s678.py` | Simulate TTS and KIS queries with strategies S4 to S4'' | `data/queries/s678.csv` |

### Experimental evaluation and results

In order to reproduce the experiments of the study, the scripts have to executed in the order shown in the following table.

| Script | Description | Output files | Reproduction of ...| 
| --- | --- | --- | --- |
| `eval/arp.py`, `eval/arp_first.py`, `eval/arp_max.py` | **Retrieval performance:** Evaluate the Average Retrieval Performance (ARP). | `data/experimental_results/arp.csv`, `data/experimental_results/arp_first.csv`, `data/experimental_results/arp_max.csv` | `Tab. A.1`  |
| `eval/rmse_s12345.py`, `eval/rmse_s678.py` | **Retrieval performance:** Evaluate the Root-Mean-Square-Error (RMSE). | `data/experimental_results/rmse_map.csv`, `data/experimental_results/rmse_ndcg.csv`, `data/experimental_results/rmse_p1000.csv`, `data/experimental_results/rmse_uqv_vs_s12345_kis_ndcg.csv`, `data/experimental_results/rmse_uqv_vs_s12345_tts_ndcg.csv`, `data/figures/rmse_map.pdf`, `data/figures/rmse_ndcg.pdf`, `data/figures/rmse_p1000.pdf`, `data/figures/rmse_uqv_vs_s12345_kis_ndcg.pdf`, `data/figures/rmse_uqv_vs_s12345_tts_ndcg.pdf` | `Fig. A.1`, `Fig. 1` |
| `eval/t-test.py` | **Retrieval performance:** Evaluate the p-values of paired t-tests. | `data/experimental_results/ttest.csv`, `data/figures/ttest.pdf` | `Fig. A.2` |
| `eval/system_orderings.py` | **Shared task utility:** Evaluate Kendall's tau between relative system orderings. | `data/experimental_results/system_orderings.csv`, `data/figures/system_orderings.pdf`  | `Fig. 2 (left)` |
| `eval/sdcg.py` | **Effort and effect:** Evaluate the Session Discounted Cumulative Gain (sDCG). | `data/experimental_results/sdcg_3queries.csv`, `data/experimental_results/sdcg_5queries.csv`, `data/experimental_results/sdcg_10queries.csv`, `data/figures/sdcg_3queries.pdf`, `data/figures/sdcg_5queries.pdf`, `data/figures/sdcg_10queries.pdf` | `Fig. 3 (top)` |
| `eval/economic.py` | **Effort and effect:** Evaluate tradeoffs between number of queries and browsing depth by isoquants. | `data/experimental_results/economic0.3.csv`, `data/experimental_results/economic0.4.csv`, `data/experimental_results/economic0.5.csv`, `data/figures/economic0.3.pdf`, `data/figures/economic0.4.pdf`, `data/figures/economic0.5.pdf` | `Fig. 3 (bottom)` | 
| `eval/jaccard_similarity.py` | **Query term similarity:** Evaluate query term similarities. | `data/experimental_results/jacc.csv`, `data/figures/jacc.pdf` | `Fig. 2 (right)` |

