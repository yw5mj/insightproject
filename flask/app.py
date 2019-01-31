from flask import Flask, request, render_template
import pandas as pd
import gensim,nltk
from util.util import *
from nltk.stem import WordNetLemmatizer

app = Flask(__name__)
@app.route('/')
def my_form():
    return render_template('my-form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    beid,bename=getbeerid(beermap,text)
    if not beid: return "beer not found"
    outp = getfeature(beid,lda_mdl,review)
    processed_text ='''
    <p><b><font size="6">Recommendation 1</font></b>:<br /><br />
    beer: <b>{0}</b> @ bar/brewery: <b>XXXXXX</b> (location: XXXXXX)<br /><br />
    dark/light: {1}<br />
    bitter/sweet: {2}<br /><br />
    <hr>
    <p><b><font size="6">Recommendation 2</font></b>:<br /><br />
    XXXXXXXX<br /><br />
    <hr>
    <p><b><font size="6">Recommendation 3</font></b>:<br /><br />
    XXXXXXXX
    '''.format(bename.upper(),outp[2][1],outp[3][1])
    return processed_text


if __name__=='__main__':
    beermap=open("/home/yanchu/work/insightproject/beeradv_crawler/data_csv/beer_id.csv").read().split('\n')
    lda_mdl= gensim.models.LdaModel.load('/home/yanchu/work/insightproject/review_nlp/models/review_lda.model')
    review=pd.read_csv('/home/yanchu/work/insightproject/review_nlp/reviews.csv',delimiter=';')
    app.run(debug=True,port=5957)

