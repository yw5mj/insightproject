#! /bin/env python
# script to map IDs for brewery/beer/style
import os,csv
class id_mapping(object):
    def __init__(self,indir="data_html",outdir="data_csv"):
        '''
        initialization
        '''
        self.indir=indir
        os.system('mkdir -p '+outdir)
        self.outdir=outdir

    def style_map(self,filename='style_id'):
        '''
        mapping style IDs
        '''
        print('>> mapping styles')
        outf=open('{0}/{1}.csv'.format(self.outdir,filename),'w')
        idwrt=csv.writer(outf,delimiter=';')
        styles=os.listdir(self.indir)
        for stid in styles:
            if stid=='styles.html': continue
            inf=open('{0}/{1}/beers.html'.format(self.indir,stid))
            stl=inf.read().split('<title>')[-1].split('</title>')[0].split('|')[0]
            idwrt.writerow([int(stid),stl])
            inf.close()
        outf.close()
    
    def beer_brew_map(self,beerf='beer_id',brewf='brew_id'):
        '''
        mapping beer and brewery IDs
        '''
        print('>> mapping breweries and beers')
        brset=set()
        bef=open('{0}/{1}.csv'.format(self.outdir,beerf),'w')
        brf=open('{0}/{1}.csv'.format(self.outdir,brewf),'w')
        bewrt=csv.writer(bef,delimiter=';')
        brwrt=csv.writer(brf,delimiter=';')
        styles=os.listdir(self.indir)
        for stid in styles:
            if stid=='styles.html': continue
            print('\t\t>> searching in style {0}'.format(stid))
            beers=os.listdir('{0}/{1}'.format(self.indir,stid))
            for beid in beers:
                if beid=='beers.html': continue
                brid=int(beid.split('_')[0])
                inf=open('{0}/{1}/{2}/page_1.html'.format(self.indir,stid,beid))
                conts=inf.read().split('<title>')[-1].split('</title>')[0].split('|')[:2]
                bewrt.writerow([beid,conts[0]])
                if brid not in brset:
                    brset.add(brid)
                    brwrt.writerow([brid,conts[1]])
                inf.close()
        bef.close()
        brf.close()


if __name__=='__main__':
    idmap=id_mapping()
    idmap.style_map()
    idmap.beer_brew_map()
