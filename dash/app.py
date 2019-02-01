import dash,gensim,pickle
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from utils import myweb,beername_matcher
import pandas as pd
from surprise import dump

app=dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.config.suppress_callback_exceptions = True

app.layout=html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page2':
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
        beer_id=recomdl.trainset.to_inner_iid(inf.id[n])
        app.in_vec=recomdl.qi[beer_id]
    except:
        return 'beer not found'
    return 'You mean "{0}" from "{1}"'.format(inf['beer'][n].strip(),inf['brewery'][n].strip())

    
@app.callback(
    Output('userid', 'children'),
    [Input('my-username', 'value')]
)
def username_fillin(input_value):
    try:
        usr_id=recomdl.trainset.to_inner_uid(input_value)
        app.in_vec=recomdl.pu[usr_id]
    except Exception as e:
        print(e)
        return 'username "{}" not found in the database'.format(input_value)
    return 'information found for user "{}"'.format(input_value)

@app.callback(
    Output('barname', 'children'),
    [Input('bars', 'value')]
)
def bar_dropdown(input_value):
    app.testlist=beerinfo[beerinfo['bar']==input_value]['beer_id']
    app.barname=input_value
    return 'You\'ve selected "{}"'.format(input_value)

if __name__=='__main__':

    dic=gensim.corpora.Dictionary.load('model/match_dict.mdl')
    tfidf = gensim.models.TfidfModel.load('model/tfidf.mdl')
    with open('model/beerX.mdl','rb') as f:X=pickle.load(f)
    with open('model/barbeer_recovec.mdl','rb') as f:bar_reco=pickle.load(f)
    recomdl=dump.load('model/RECOMDL.mdl')[1]
    inf=pd.read_csv('/home/yanchu/work/insightproject/beeradv_crawler/data_csv/beer_id.csv',';')
    beerinfo=pd.read_csv('/home/yanchu/work/insightproject/cleandata/final.csv')
    bars=list(set(beerinfo['bar']))
    bars.sort()
    app.run_server(debug=True)
