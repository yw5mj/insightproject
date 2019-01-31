#! /bin/env python
import pickle
import numpy as np
import pandas as pd
from surprise import *
mdl=dump.load('model/RECOMDL.mdl')[1]
ids=set(pd.read_csv("/home/yanchu/work/insightproject/cleandata/bid_name_review.csv")['id'])
inid=[(i,mdl.trainset.to_inner_iid(i)) for i in ids]
dic={i[0]:mdl.qi[i[1]] for i in inid}
with open('model/barbeer.mdl','wb') as f: pickle.dump(dic,f)
