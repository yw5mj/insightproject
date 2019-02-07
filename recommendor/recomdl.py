#! /bin/env python

import pandas as pd
from surprise.utils import get_rng
from surprise import *
import random

def init_qi(algos,trainset):
    rng = get_rng(algos.random_state)
    algos.qi=rng.normal(algos.init_mean, algos.init_std_dev,(trainset.n_items, algos.n_factors))
    df=pd.read_csv("/home/yanchu/work/insightproject/review_nlp/allbeer_features.csv")[['id','bitter','sweet','sour']]
    tot=df.bitter+df.sweet+df.sour
    df['bitter']=df['bitter']/tot
    df['sweet']=df['sweet']/tot
    df['sour']=df['sour']/tot
    df=df.values
    for dt in df:
        iid=trainset.to_inner_iid(int(dt[0]))
        algos.qi[iid][:3]=dt[1:4]

df=pd.read_csv("/home/yanchu/work/insightproject/beeradv_crawler/data_csv/allbeers.csv",delimiter=';')
df=df[['usr_name','beer_id','rating']]
data = Dataset.load_from_df(df,rating_scale=(1,5))
random.shuffle(data.raw_ratings)
trainset = data.build_full_trainset()
algos=SVD(n_factors=40,reg_bu=0.9,reg_bi=0.9,rand_qi=False)
init_qi(algos,trainset)
algos.fit(trainset)
#model_selection.cross_validate(algos, data, measures=['RMSE', 'MAE'], cv=3, verbose=True)
dump.dump('RECOMDL.mdl',algo=algos)

'''
mdl=algos
output=np.dot(mdl.pu,mdl.qi.transpose())
output+=mdl.bi
for n,u in enumerate(output):
    if n<300:
        print(max(enumerate(u),key=lambda x:x[1]))
'''
