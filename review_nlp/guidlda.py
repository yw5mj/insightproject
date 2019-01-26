#! /bin/env python
import numpy as np
import gensim,nltk,sys
from nltk.stem import WordNetLemmatizer
import pandas as pd
import guidedlda
def pre_process(inp):
    lemm=WordNetLemmatizer()
    temp=[lemm.lemmatize(word.lower()) for word in gensim.utils.tokenize(inp.replace("ness",'')) if len(word)>3 and (word not in gensim.parsing.preprocessing.STOPWORDS)]
    temp=[i[0] for i in nltk.pos_tag(temp) if i[1] in {'NN','JJ'}]
    ignset={"beer","nice","good","great","glass","drink","brew","bottle"}
    temp=[i for i in temp if i not in ignset]
    return temp

def seed_ids(dic):
    seeds=[
        ['bitter','earthy','malt','hop'],
        ['chocolate','dark','black'],
        ['sweet','honey','fruit'],
        ['golden','clear','light']
        ]
    w2id={dic[i]:i for i in dic}
    return [[w2id[i] for i in t] for t in seeds]
if __name__=='__main__':
    inf=[pre_process(i) for i in pd.read_csv('every_review.csv')['review'][::20]]
    dic=gensim.corpora.Dictionary(inf)
    dic.filter_extremes(no_below=500, no_above=1, keep_n=5000)
    corpus=[dic.doc2bow(i) for i in inf]
    tfidf = gensim.models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    X=np.transpose(gensim.matutils.corpus2csc(corpus_tfidf).astype(np.float))
    glda_mdl=guidedlda.GuidedLDA(n_topics=4, n_iter=100, random_state=7, refresh=20)
    glda_mdl.fit(X,seed_topics=seed_ids(dic), seed_confidence=0.15)
