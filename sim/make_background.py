import os; os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64/"
import pandas as pd
from config import default as config
from pyserini.index import IndexReader

index_reader = IndexReader(config['PATH_IDX'])


def _normalize(row, cf_sum):
    return row['cf'] / cf_sum


def main():
    df = pd.DataFrame.from_dict({term.term: {'df': term.df, 'cf': term.cf} for term in index_reader.terms()})
    df = df.transpose()
    cf_sum = df['cf'].sum()
    df['prob'] = df.apply (lambda row: _normalize(row, cf_sum), axis=1)
    df.to_csv('data/lm/background.csv')


if __name__ == '__main__':
    main()
