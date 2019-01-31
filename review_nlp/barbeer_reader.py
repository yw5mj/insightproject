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

def process_rv(inp,dic,tfidf,glda_mdl):
    prcsed=pre_process(inp)
    corpus=dic.doc2bow(prcsed)
    corpus_tfidf = tfidf[corpus]
    X=np.transpose(gensim.matutils.corpus2csc(corpus_tfidf).astype(np.float))
    X=(X*1000).astype(np.int64)
    
    
if __name__=='__main__':
    dic=gensim.corpora.Dictionary.load('models/dictionary/dict.mdl')
    tfidf = gensim.models.TfidfModel.load('models/tfidf/tfidf.mdl')
    with open('models/guidedlda/glda.pkl', 'rb') as file_handle:
        glda_mdl=pickle.load(file_handle)
    inm=pd.read_csv('/home/yanchu/work/insightproject/cleandata/bid_name_review.csv')
    inf=[pre_process(i) for i in inm['review']]
    corpus=[dic.doc2bow(i) for i in inf]
    corpus_tfidf = tfidf[corpus]
    X=np.transpose(gensim.matutils.corpus2csc(corpus_tfidf).astype(np.float))
    X=(X*1000).astype(np.int64)
    doc_topic = glda_mdl.transform(X)
    ftrs=pd.DataFrame(doc_topic,columns=['bitter', 'dark', 'sweet', 'light', 'sour','nonsense'])
    ftrs.drop(columns=['nonsense'],inplace=True)
    output=inm[['id','name']].join(ftrs)
    output.to_csv("beer_features.csv",index=False)

