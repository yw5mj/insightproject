import pandas as pd
import csv
inf=pd.read_csv('../cleandata/allbeers.csv',delimiter=';')
inf=inf[['beer_id', 'review']].dropna()
beset=set(inf['beer_id'])
f=open('reviews.csv','w')
csvw=csv.writer(f,delimiter=';')
csvw.writerow(['id','review'])
for beer in beset:
    subset=inf[inf['beer_id']==beer]
    csvw.writerow([beer,' '.join(subset['review'][:100])])
f.close()
