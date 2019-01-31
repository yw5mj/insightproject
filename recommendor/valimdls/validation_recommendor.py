#! /bin/env python

import pandas as pd
from surprise import *
import sys
df=pd.read_csv("/home/yanchu/work/insightproject/beeradv_crawler/data_csv/allbeers.csv",delimiter=';')
df=df[['usr_name','beer_id','rating']]
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df,reader)
algos=SVD(n_factors=int(sys.argv[1]),reg_bu=0.9,reg_bi=0.9)
model_selection.cross_validate(algos, data, measures=['RMSE', 'MAE'], cv=3, verbose=True)




