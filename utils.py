import pandas as pd
import itertools


def _uqv(filename='./data/robust-uqv.txt'):
    with open(filename, 'r') as f_in:
        for line in f_in.readlines():
            topic_user_query = line.split(';')[0].split('-')
            qstr = line.split(';')[1].strip('\n')
            yield {'topic': int(topic_user_query[0]),
                   'user': int(topic_user_query[1]),
                   'num': int(topic_user_query[2]),
                   'qstr': qstr,
                   'reformulation': int(topic_user_query[2]) > 1}


def parse_uqv(filename='./data/robust-uqv.txt'):
    # Still used in some older scripts
    return pd.DataFrame.from_dict(_uqv(filename=filename))


def uqv(filename='./data/robust-uqv.txt'):
    return pd.DataFrame.from_dict(_uqv(filename=filename))


def take(n, iterable):
    return list(itertools.islice(iterable, n))


def sort_dict(dictionary):
    return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse=True)}


def qcmcqg(filename='data/qcmcqg_queries.csv'):
    return pd.read_csv(filename)


def trec(filename='data/trec_queries.csv'):
    return pd.read_csv(filename)


def parse_results(pyserini_results, topic):
    return {topic: {result.docid: len(pyserini_results)-i for i, result in enumerate(pyserini_results)}}
