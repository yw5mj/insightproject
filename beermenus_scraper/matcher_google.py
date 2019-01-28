import pandas as pd
import csv, time
import numpy as np
from selenium import webdriver

keystr='href="https://www.beeradvocate.com/beer/profile/'
def one_beer(drv,beername):
    sbm=drv.find_element_by_name("q")
    sbm.clear()
    sbm.send_keys(beername+' beeradvocate')
    sbm.submit()
    time.sleep(np.random.normal(5,2.5))
    cont=drv.page_source
    if keystr not in cont:
        print(beername)
    else:
        output=cont.split(keystr)[1].split('"')[0].split('/')
        if len(output)!=3:
            print(beername)
            return
        return '_'.join(output[:2])

drv=webdriver.Firefox()
drv.get("https://www.google.com/")

innames=set(pd.read_csv("bars.csv",delimiter=';')['beer'])
dones=set(pd.read_csv('name_id_matcher.csv',delimiter=';')['name'])
with open('name_id_matcher.csv','a+') as f:
    wrt=csv.writer(f,delimiter=';')
#    wrt.writerow(["name",'id'])
    for i in innames:
        if i in dones:
            print('skipping ',i)
            continue
        fail=True
        while fail:
            fail=False
            try:
                outp=one_beer(drv,i)
            except Exception as e:
                print(e)
                time.sleep(30)
                fail=True
        if outp:
            wrt.writerow([i,outp])
drv.quit()        
    
