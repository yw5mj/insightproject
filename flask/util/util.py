#! /bin/env python

from util.lda import pre_process
def getbeerid(inf,bname):
    bname=bname.lower().strip()
    output,dif=(0,0),100000
    for i in inf:
        if i.strip():
            beern=i.split(';')[1].lower().strip()
            beeid=int(i.split(';')[0].split('_')[1])
            if (bname in beern) or (beern in bname):
#                print(dif,beern)
                if dif>abs(len(beern)-len(bname)):
                    output=(beeid,beern)
                    dif=abs(len(beern)-len(bname))
    return output
def getfeature(beid,model,review):
    rv=review[review['id']==beid]['review'].iloc[0]
    corpus=model.id2word.doc2bow(pre_process(rv))
    return model.get_document_topics(corpus)


    
