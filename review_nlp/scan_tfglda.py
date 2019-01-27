#! /bin/env python
import numpy as np
import gensim,nltk
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
    return {w2id[i]:n for n,x in enumerate(seeds) for i in x}
if __name__=='__main__':
    inf=[pre_process(i) for i in pd.read_csv('every_review.csv')['review'][::20]]
    dic=gensim.corpora.Dictionary(inf)
    dic.filter_extremes(no_below=10, no_above=1, keep_n=5000)
    corpus=[dic.doc2bow(i) for i in inf]
    tfidf = gensim.models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    X=np.transpose(gensim.matutils.corpus2csc(corpus_tfidf).astype(np.float))
    X=(X*100).astype(np.int64)
    seeds=seed_ids(dic)
    vocab=list(dic.values())
    for n in range(4,25,4):
        f=open('scan_{0}.txt'.format(n),'w')
        glda_mdl=guidedlda.GuidedLDA(n_topics=n, n_iter=100, random_state=7, refresh=20)
        glda_mdl.fit(X,seed_topics=seeds, seed_confidence=0.15)
        topic_word = glda_mdl.topic_word_
        for i, topic_dist in enumerate(topic_word):
            topic_words = np.array(vocab)[np.argsort(topic_dist)][:-9:-1]
            f.write('Topic {}: {}\n'.format(i, ' '.join(topic_words)))
        f.write('LL: {0}'.format(glda_mdl.loglikelihood()))
        f.close()
