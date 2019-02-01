import dash
import dash_core_components as dcc
import dash_html_components as html

bkg_clr='#FFFAFA'
ttl_clr='#E9967A'
def page1(bars):
    return html.Div(style={'backgroundColor': bkg_clr}, children=[
    html.H1(children='Beerston!',style={'textAlign': 'center','color': ttl_clr}),
    html.Hr(),
    html.H2(children='Step 1',style={'textAlign': 'center'}),
    html.Div(children='Enter the bar you are in:'),
    dcc.Dropdown(id='bars',options=[{'label':i,'value':i} for i in bars],value='None'),
    html.Div(id='barname'),
    html.Hr(),
    html.H2(children='Step 2',style={'textAlign': 'center'}),
    html.Div(children='Enter your beeradvocate.com username:'),
    dcc.Input(id='my-username', value='', type='text'),
    html.Div(id='userid'),
    html.Br(),
    html.Br(),
    html.H6(children="Don't have a beeradvocate.com account? No worries!"),
    html.Div(children="Enter your favourite beer name:"),
    dcc.Input(id='my-beer', value='', type='text'),
    html.Div(id='beerid'),
    html.Hr(),
    html.Div(style={'textAlign': 'center'}, children=[
    html.Div(children="Now get recommendations!"),
    html.Br(),
    html.A(html.Button('Submit'),href='/page2')])
])

def page2(inp,beerinfo,barname):
    output=[html.H1(children='Beers@{0}'.format(barname),style={'textAlign': 'center','color': ttl_clr}),
    html.Hr(),
]
    for n,i in enumerate(inp):
        output.append(html.H2(children='Recommendation {}'.format(n+1),style={'textAlign': 'center'}))
        output.extend(recom(int(i),beerinfo))
    return html.Div(style={'backgroundColor': bkg_clr}, children=output)

def recom(beerid,beerinfo):
    info=beerinfo[beerinfo['beer_id']==beerid]
    allflavor=info['bitter'].iloc[0]+info['sweet'].iloc[0]+info['sour'].iloc[0]
    return [html.H3(children=info['beer'].iloc[0]),
            html.Div(children='bitterness: {0}%'.format(int(info['bitter'].iloc[0]/allflavor*100))),
            html.Div(children='sweetness: {0}%'.format(int(info['sweet'].iloc[0]/allflavor*100))),
            html.Div(children='sourness: {0}%'.format(int(info['sour'].iloc[0]/allflavor*100))),
            html.Div(children='serve: {0}'.format(info['serve'].iloc[0].replace('|',' | '))),
            html.Div(children='info: {0}'.format(info['info'].iloc[0])),
            html.Div(children='Beeradvocate score: {0}/5'.format(info['BA_score'].iloc[0])),
            html.Hr()
    ]
    
