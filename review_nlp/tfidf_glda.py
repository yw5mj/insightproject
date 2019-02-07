#! /bin/env python
from six.moves import cPickle as pickle
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
        ['bitter','hop'],
        ['chocolate','dark','black'],
        ['sweet','honey','sugar'],
        ['golden','clear','light'],
        ['sour','vinegar']
        ]
    w2id={dic[i]:i for i in dic}
    return {w2id[i]:n for n,x in enumerate(seeds) for i in x}

if __name__=='__main__':
    inf=[pre_process(i) for i in pd.read_csv('every_review.csv')['review'][::20]]
    dic=gensim.corpora.Dictionary(inf)
    dic.filter_extremes(no_below=10, no_above=1, keep_n=5000)
    dic.save('models/dictionary/dict.mdl')
    corpus=[dic.doc2bow(i) for i in inf]
    tfidf = gensim.models.TfidfModel(corpus)
    tfidf.save('models/tfidf/tfidf.mdl')
    corpus_tfidf = tfidf[corpus]
    X=np.transpose(gensim.matutils.corpus2csc(corpus_tfidf).astype(np.float))
    X=(X*1000).astype(np.int64)
    glda_mdl=guidedlda.GuidedLDA(n_topics=6, n_iter=100, random_state=7, refresh=20)
    glda_mdl.fit(X,seed_topics=seed_ids(dic), seed_confidence=0.15)
    with open('models/guidedlda/glda.pkl', 'wb') as file_handle:
        pickle.dump(glda_mdl, file_handle)
    vocab=list(dic.values())
    topic_word = glda_mdl.topic_word_
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-9:-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))
