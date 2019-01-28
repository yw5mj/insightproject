#! /bin/env python
# script to parse html files from beermenus
import os,csv
def parser_bar(inf='data_html/13727-culpeppers-pub-grill.html',csvw=None):
    with open(inf) as f:
        cont=f.read()
        barname=cont.split('<h1 class="mb-0 text-biggest">')[-1].split('</h1>')[0].strip().replace("&amp;",'&')
        locat=cont.split("MapClicks")[-1].split('</a>')[0].split('>')[-1]
        allbrs=cont.split('<h3 class="mb-0 text-normal">')[1:]
        for i in allbrs:
            bname=i.split('>')[1].split('<')[0]
            info1=' '.join(i.split('<p class="caption text-gray mb-0">')[1].split('</p>')[0].replace('·','|').split())
            try:
                info2='|'.join(i.split('<p class="caption text-right mb-0 last">')[1].split('</p>')[0].split())
            except:
                print("ERROR: {0} in {1}".format(bname,inf))
                continue
            if csvw:
                csvw.writerow([barname,locat,bname,info1,info2])
                
def parse_all(indir='data_html',outf='bars.csv'):
    infs=os.listdir(indir)
    f=open(outf,'w')
    csvwrt=csv.writer(f,delimiter=';')
    csvwrt.writerow(['bar','location','beer','info','serve'])
    for inf in infs:
        parser_bar('{0}/{1}'.format(indir,inf),csvwrt)



if __name__=='__main__':
    parse_all()
