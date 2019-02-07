import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

bkg_clr='#FFFAFA'
ttl_clr='#E9967A'
dark_layout = go.Layout(
    xaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=False,
        zeroline=False,
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        zeroline=False,
        domain=[0.4, 0.6]
    ),
    barmode='stack',
    paper_bgcolor='rgb(255,250,250)',
    plot_bgcolor='rgb(255,250,250)',
    showlegend=False,
)

def page1(bars):
    return html.Div(style={'backgroundColor': bkg_clr}, children=[
    html.H1(children='Brewston',style={'textAlign': 'center','color': ttl_clr}),
    html.H6(children='Find your beer in Boston bars',style={'textAlign': 'center'}),
    html.Hr(),
    html.H2(children='Step 1',style={'textAlign': 'center'}),
    html.Div(children='Enter the bar you are in:'),
    dcc.Dropdown(id='bars',options=[{'label':i,'value':i} for i in bars],value='Town Wine and Spirits'),
    html.Div(id='barname'),
    html.Hr(),
    html.H2(children='Step 2',style={'textAlign': 'center'}),
    html.Div(children='Enter your beeradvocate.com username:'),
    dcc.Input(id='my-username', value='zimm421', type='text'),
    html.Div(id='userid'),
    html.Br(),
    html.Br(),
    html.H6(children="Don't have a beeradvocate.com account? No worries!"),
    html.Div(children="Enter your favourite beer name:"),
    dcc.Input(id='my-beer', value='limbo ipa', type='text'),
    html.Div(id='beerid'),
    html.Hr(),
    html.Div(style={'textAlign': 'center'}, children=[
    html.Div(children="Now get recommendations!"),
    html.Br(),
    html.A(html.Button('Submit'),href='/recommendations')])
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
    tags=['type','ABV','from']
    info=beerinfo[beerinfo['beer_id']==beerid]
    allflavor=info['bitter'].iloc[0]+info['sweet'].iloc[0]+info['sour'].iloc[0]
    flavors=[int(info['bitter'].iloc[0]/allflavor*100),int(info['sweet'].iloc[0]/allflavor*100),int(info['sour'].iloc[0]/allflavor*100)]
    clrs=int(100*info['dark'].iloc[0]/(info['dark'].iloc[0]+info['light'].iloc[0]))
    serve=info['serve'].iloc[0].split('|')
    serve[1]='({})'.format(serve[1])


    return [html.H3(children=info['beer'].iloc[0]),
            html.Div([
                html.Div(
                    [dcc.Graph(figure={'data':[go.Pie(labels=['bitter','sweet','sour'],values=flavors)],'layout':go.Layout(paper_bgcolor='rgb(255,250,250)',plot_bgcolor='rgb(255,250,250)')})],style={'width': '20%', 'display': 'inline-block'},
                    className="six columns"),
                html.Div(
#                    [dcc.Graph(figure={'data':[go.Bar(y=['darkness'],x=[clrs],orientation = 'h',marker={'color':'rgba(38, 24, 74, 0.8)'}),go.Bar(y=['darkness'],x=[100-clrs],orientation = 'h',marker={'color':'rgba(164, 163, 204, 0.85)'})],'layout':dark_layout})],style={'width': '20%', 'display': 'inline-block'},
                    [dcc.Graph(figure={'data':[go.Bar(y=['darkness'],x=[clrs],orientation = 'h',marker={'color':'rgba(178,34,34,0.8)'}),go.Bar(y=['darkness'],x=[100-clrs],orientation = 'h',marker={'color':'rgba(238,232,170,0.85)'})],'layout':dark_layout})],style={'width': '20%', 'display': 'inline-block'},
                    className="six columns"),
                html.Div([html.Br()]*7+[
                    html.Div(children='Beeradvocate score: {0}/5'.format(info['BA_score'].iloc[0])),
                    html.Div(children='serve: {0}'.format(' '.join(serve))),
                    ]+[html.Div(children='{0}:{1}'.format(tags[n],i)) for n,i in enumerate(str(info['info'].iloc[0]).split('|')[:3])]
                         , className="six columns")],className="row"),
            html.Hr()
    ]
    
