#! /bin/env python
import numpy as np
import gensim
import pandas as pd
import pickle,sys

def pre_process(inp):
    from nltk.stem import WordNetLemmatizer
    lemm=WordNetLemmatizer()
    temp=[lemm.lemmatize(word.lower()) for word in gensim.utils.tokenize(inp.replace("'",'').replace('&',''))]
    ignset={"company",'brewing','brewer','brewery','beer'}
    temp=[i for i in temp if i not in ignset]
    return temp

def get_match(inp,dic,X,tfidf):
    inp=pre_process(inp)
    corpus=[dic.doc2bow(inp)]
    corpus_tfidf = tfidf[corpus]
    vec=gensim.matutils.corpus2csc(corpus_tfidf,num_terms=X.shape[0]).transpose()
    mats=vec.dot(X)
    return max(enumerate(mats.toarray()[0]),key=lambda x:x[1])[0]

if __name__=='__main__':
    dic=gensim.corpora.Dictionary.load('model/match_dict.mdl')
    tfidf = gensim.models.TfidfModel.load('model/tfidf.mdl')
    with open('model/beerX.mdl','rb') as f:X=pickle.load(f)
    inf=pd.read_csv('/home/yanchu/work/insightproject/beeradv_crawler/data_csv/beer_id.csv',';')
    n=get_match(sys.argv[1],dic,X,tfidf)
    print(inf['beer'][n])
