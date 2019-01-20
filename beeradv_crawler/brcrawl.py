#! /bin/env python
# functions to scrape reviews for beers from beeradvocate

import requests
import time,os
def getcon(url,delta=1):
    '''
    get webpage content from beeradvocate
    '''
    url='https://www.beeradvocate.com'+url
    start = time.time()
    cont = requests.get(url).content
    if time.time()-start<delta:
        time.sleep(delta-(time.time()-start))
    return cont

def crawl_beer(url='/beer/profile/628/5119/',outdir='temp'):
    '''
    get info for a beer
    '''
    os.system("mkdir -p "+outdir)
    pgs,n='',0
    while True:
        print '\t\t>> page: ',n
        pgs,n=getcon(url),n+1
        with open("{0}/page_{1}.html".format(outdir,n),'w') as outf: outf.write(pgs)
        temps=[i for i in pgs.split(';') if '>next</a>' in i and '<a href=' in i]
        if not temps: break
        try:
            url=temps[0].split('"')[1]
        except:
            print 'ERROR:\n',temps
            break
    return
    
def crawl_style(url='/beer/styles/8/',outdir='temp'):
    '''
    crawl all beers in the same style
    considering number of beer products is infinite but my harddrive capacity is not, in each style I only scrape 50 most popular beers.
    '''
    os.system("mkdir -p "+outdir)
    beers=getcon(url)
    with open("{0}/beers.html".format(outdir),'w') as outf: outf.write(beers)
    beers=[i for i in beers.split('"') if '/beer/profile/' in i]
    for i in beers:
        tag1,tag2=i.split('/')[-3:-1]
        if tag1.isdigit() and tag2.isdigit():
            print '\t>> beer: {0}/{1}_{2}'.format(outdir,tag1,tag2)
            crawl_beer(i,'{0}/{1}_{2}'.format(outdir,tag1,tag2))

def crawl_all(outdir='temp'):
    '''
    crawl all beers
    '''
    os.system("mkdir -p "+outdir)
    styles=getcon('/beer/styles/')
    with open("{0}/styles.html".format(outdir),'w') as outf: outf.write(styles)
    styles=[i for i in styles.split('"') if '/beer/styles/' in i]
    for i in styles:
        tag=i.split('/')[-2]
        if tag.isdigit():
            print '>> style: {0}/{1}'.format(outdir,tag)
            crawl_style(i,'{0}/{1}'.format(outdir,tag))
    

    
