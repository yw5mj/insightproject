#! /bin/env python
# scripts to parse beeradvocate htmls
import os,csv
def parse_beer(indir='data_html/52/25888_103496/',csvwrt=None):
    '''
    parser for a beer
    '''
    fls=os.listdir(indir)
    page1=open(indir+'/page_1.html')
    cont=page1.read()
    outlist1=indir.split('/')[-1].split('_')
    outlist1.append(indir.split('/')[-2])
    outlist1.append(float(cont.split('<span class="ba-ravg">')[-1].split('</span>')[0]))
    abv=cont.split('(ABV):</b>')[-1].split('\n')[0].split('%')[0]
    outlist1.append(float(abv) if 'not listed' not in abv else None)
    page1.close()
    for i in fls:
        inf=open('{0}/{1}'.format(indir,i))
        cont=inf.read()
        reviews=[i.split('class="username">')[0] for i in cont.split('<span class="BAscore_norm">')[1:]]
        for j in reviews:
            outlist2=j.split('"/community/members/')[-1].split('.')
            usrid=outlist2[1].strip().strip('/"')
            if not usrid: continue
            outlist2[1]=int(usrid)
            rvw=j.split('</span><br><br>')
            outlist2.append(float(rvw[0].split('</span>')[0]))
            if 'smell:' in rvw[0]:
                outlist2.extend([float(x) for x in rvw[0].split('look:')[-1].split(' ') if x and x[0].isdigit()])
            else:
                outlist2.extend([None]*5)
            if len(rvw)>2:
                outlist2.append(rvw[1].split('<br><br>')[0].replace("<br />",'').replace("\n",' '))
            else: outlist2.append(None)
            if csvwrt: csvwrt.writerow(outlist1+outlist2)
            else: print(outlist1+outlist2)

def parse_style(indir='data_html/10/',csvwrt=None):
    '''
    parser for a style of beers
    '''
    beers=os.listdir(indir)
    for i in beers:
        if i=='beers.html':continue
        try:
            parse_beer('{0}/{1}'.format(indir,i),csvwrt)
        except Exception as e:
            print('{0}/{1}'.format(indir,i), e)


def parse_all(indir='data_html/',outf='data_csv/allbeers.csv'):
    '''
    parser for all beers
    '''
    f=open(outf,'w')
    csvwrt=csv.writer(f,delimiter=';')
    csvwrt.writerow(['brew_id','beer_id','style_id','BA_score','ABV','usr_name','usr_id','rating','look','smell','taste','feel','overall','review'])
#    csvwrt=None
    styles=os.listdir(indir)
    for i in styles:
        if i=="styles.html":continue
        parse_style('{0}/{1}'.format(indir,i),csvwrt)
    f.close()

if __name__=='__main__':
    parse_all()

    
    
        
            
        
        
