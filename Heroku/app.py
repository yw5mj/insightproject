import dash,gensim,pickle
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from utils import myweb,beername_matcher
import pandas as pd


app=dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

server = app.server
app.title='Brewston'

dic=gensim.corpora.Dictionary.load('model/NLP_match_dict.mdl')
tfidf = gensim.models.TfidfModel.load('model/NLP_tfidf.mdl')
with open('model/NLP_beerX.mdl','rb') as f:X=pickle.load(f)

with open('model/CF_barbeer_recovec.mdl','rb') as f:bar_reco=pickle.load(f)
with open('model/CF_iid.mdl','rb') as f: iid_reco=pickle.load(f)
with open('model/CF_uid.mdl','rb') as f: uid_reco=pickle.load(f)
with open('model/CF_qi.mdl','rb') as f: qi_reco=pickle.load(f)
with open('model/CF_pu.mdl','rb') as f: pu_reco=pickle.load(f)

inf=pd.read_csv('data_csv/beer_id.csv',';')
beerinfo=pd.read_csv('data_csv/final.csv')
bars=list(set(beerinfo['bar']))
bars.sort()

app.config.suppress_callback_exceptions = True

app.layout=html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/recommendations':
        if not hasattr(app,"in_vec"):
            return html.Div([html.Div('Please tell us your beeradvocate username or favourite beer.')])
        if not hasattr(app,"testlist"):
            return html.Div([html.Div('Please choose the bar.')])
        scores=[(i,bar_reco[i].dot(app.in_vec)) for i in app.testlist]
        scores.sort(key=lambda x:x[1],reverse=True)
        return myweb.page2([i[0] for i in scores[:3]],beerinfo,app.barname)
    else:
        return myweb.page1(bars)
    
@app.callback(
    Output('beerid', 'children'),
    [Input('my-beer', 'value')]
)
def beer_fillin(input_value):
    try:
        n=beername_matcher.get_match(input_value,dic,X,tfidf)
        beer_id=iid_reco[inf.id[n]]
        app.in_vec=qi_reco[beer_id]
    except:
        return 'beer not found'
    return 'Do you mean "{0}" from "{1}"?'.format(inf['beer'][n].strip(),inf['brewery'][n].strip())

    
@app.callback(
    Output('userid', 'children'),
    [Input('my-username', 'value')]
)
def username_fillin(input_value):
    try:
        usr_id=uid_reco[input_value]
        app.in_vec=pu_reco[usr_id]
    except Exception as e:
        return 'username "{}" not found in the database'.format(input_value)
    return 'information found for user "{}"'.format(input_value)

@app.callback(
    Output('barname', 'children'),
    [Input('bars', 'value')]
)
def bar_dropdown(input_value):
    app.testlist=set(beerinfo[(beerinfo['bar']==input_value) & (beerinfo["BA_score"]>3.25)]['beer_id'])
    app.barname=input_value
    return 'You\'ve selected "{}"'.format(input_value)

if __name__=='__main__':
    app.run_server(debug=True)
