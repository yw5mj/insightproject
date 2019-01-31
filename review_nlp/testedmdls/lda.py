#! /bin/env python                                                                                                                                                                                                 
import gensim,nltk
from nltk.stem import WordNetLemmatizer
import pandas as pd

def pre_process(inp):
    lemm=WordNetLemmatizer()
    temp=[lemm.lemmatize(word.lower()) for word in gensim.utils.tokenize(inp.replace("ness",'')) if len(word)>3 and (word not in gensim.parsing.preprocessing.STOPWORDS)]
    temp=[i[0] for i in nltk.pos_tag(temp) if i[1] in {'NN','JJ'}]
    ignset={"beer","nice","good","great","glass","drink","brew","bottle"}
    temp=[i for i in temp if i not in ignset]
    return temp
if __name__=='__main__':
    inf=[pre_process(i) for i in pd.read_csv('every_review.csv')['review'][::20]]
    dic=gensim.corpora.Dictionary(inf)
    dic.filter_extremes(no_below=500, no_above=1, keep_n=5000)
    corpus=[dic.doc2bow(i) for i in inf]
    lda_mdl = gensim.models.LdaMulticore(corpus, num_topics=20, id2word=dic, passes=2)
    #lda_mdl.save('review_lda.model')
    for idx, topic in lda_mdl.print_topics(-1):
        print('Topic: {} \nWords: {}'.format(idx, topic))
 
