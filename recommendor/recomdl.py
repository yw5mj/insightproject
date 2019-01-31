#! /bin/env python

import pandas as pd
from surprise import *
import random
df=pd.read_csv("/home/yanchu/work/insightproject/beeradv_crawler/data_csv/allbeers.csv",delimiter=';')
df=df[['usr_name','beer_id','rating']]
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df,reader)
random.shuffle(data.raw_ratings)
trainset = data.build_full_trainset()
algos=SVD(n_factors=40,reg_bu=0.9,reg_bi=0.9)
algos.fit(trainset)
dump.dump('RECOMDL.mdl',algo=algos)

'''
mdl=algos
output=np.dot(mdl.pu,mdl.qi.transpose())
output+=mdl.bi
for n,u in enumerate(output):
    if n<300:
        print(max(enumerate(u),key=lambda x:x[1]))
'''
