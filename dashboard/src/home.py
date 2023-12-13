#!/usr/bin/env python3

#import sys
#sys.path.append("/home/cm/innovhope_projects/dashboard_latest/utils/")

from dash import dcc, html
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.express as px

import re
import requests

from utils.constants import api_key
from utils.download_preprocess import *
from utils.links import *
from utils.columns import *
from utils.queries import *
from utils.transformers import *
from utils.nlp import *
from utils.ml import *
from utils.utils import *

from app import app

config_file = get_path() + 'config.txt'
dl = DataLoader()
df_ml = dl.load_data_ml()

options_categorical = make_options(
    {k:k for k in options_categorical_features}
)
options_funding = make_options(
    {k:k for k in options_funding_features}   
)
options_time = make_options(
    {k:k for k in options_time_features}  
)

# Create app layout
layout = html.Div(
    [
        dcc.Store(id="analyze-data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(
            [
                html.H3("Search Intelligence")
            ],
            className="one-half column",
        ),
        html.Div(
            [
                html.H3("1. Update the database and ML models")
            ],
            className="one-half column",
        ),
        html.Div(
            [
                html.Button(
                    '1. Update Crunchbase database (around 50 mins)', 
                    id='update-crunchbase', 
                    n_clicks=0,
                    style={
                        "width":"650px",
                        "margin-right":"10px"
                    }
                ),
                html.Button(
                    '2. Re-train models and select the best one', 
                    id='retrain-models', 
                    n_clicks=0,
                    style={
                        "width":"650px"
                    }
                ),
            ],
            className="pretty_container twelve columns",
            id="database-model-updates",
        ),
        html.Div(
            [
                html.H3("2. Search Company of Interest")
            ],
            className="one-half column",
        ),
        html.Div(
            [
                dcc.Input(
                    id='keywords-list-tag',
                    type='text',
                    value=None,
                    placeholder='Tag (e.g, vaccine)',
                    size="lg",
                    style={
                        "width":"300px",
                        "margin-right":"10px"
                    }
                ),
                dcc.Input(
                    id='keywords-list',
                    type='text',
                    value=None,
                    placeholder='Search keywords: similar search terms (e.g., covid-19 vaccine, covid19 vaccine, sars-cov-2 vaccine)',
                    size="lg",
                    style={
                        "width":"750px",
                        "margin-right":"10px"
                    }
                ),
                html.Button(
                    'Search (around 45 mins)', 
                    id='search-company-submit-val', 
                    n_clicks=0,
                    style={
                        "width":"240px",
                    }
                ),
            ],
            className="pretty_container twelve columns",
            id="search-results",
        ),
        html.Div(
             [
                html.Div(
                    dbc.Spinner(
                        [dcc.Graph(id='map-graph')], 
                        color='light'
                    ),
                    id='global-distribution',
                ),
             ],
             className="pretty_container twelve columns",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H4(
                            "Summary of Search Results",
                            className='control_label',
                        ),
                    ],
                    id="company-search-summary",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H6(
                                    "Select a time feature",
                                    className='control_label',
                                ),
                                dcc.Dropdown(
                                    id='time',
                                    options=options_time,
                                    multi=False,
                                    value='founded_on',
                                    className='dcc_control',
                                ),
                                html.Div(
                                    [dcc.Graph(id='time-statistics')]
                                ),
                            ],
                            className="pretty_container three columns",
                            id="time-options",
                        ),
                        html.Div(
                            [
                                html.H6(
                                    "Select a categorical feature",
                                    className='control_label',
                                ),
                                dcc.Dropdown(
                                    id='categorical',
                                    options=options_categorical,
                                    multi=False,
                                    value='country_code',
                                    className='dcc_control',
                                ),
                                html.Div(
                                    [dcc.Graph(id='categorical-statistics')]
                                ),
                            ],
                            className="pretty_container four columns",
                            id="categorical-options",
                        ),
                        html.Div(
                            [
                                html.H6(
                                    "Select a funding feature",
                                    className="control_label",
                                ),
                                dcc.Dropdown(
                                    id='continuous',
                                    options=options_funding,
                                    multi=False,
                                    value='series_a',
                                    className='control_label',
                                ),
                                html.Div(
                                    [dcc.Graph(id='continuous-statistics')]
                                ),
                            ],
                            className="pretty_container four columns",
                            id="continuous-options",
                        ),
                    ],
                ),
            ],
            className="pretty_container twelve columns",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H4(
                            "Select a Company",
                            className='control_label',
                        ),
                        html.Br(),
                        dcc.Dropdown(
                            id='companies',
                            multi=False,
                            className='control_label',
                        ),
                    ],
                    className="pretty_container three columns",
                    id="company-search-results",
                ),
                # html.Div(
                #     [
                #         html.H4(
                #             "Founders",
                #             className="control_label",
                #         ),
                #         html.Br(),
                #         html.Div(
                #             id="company-founders",
                #             style={
                #                 'height':15,
                #                 "margin-left":"10px",
                #                 "color":'black',
                #                 "fontSize": 20
                #             },
                #         ),
                #     ],
                #     className="pretty_container two columns",
                # ),
                html.Div(
                    [
                        html.H4(
                            "HQ Location",
                            className="control_label",
                        ),
                        html.Br(),
                        html.Div(
                            id="company-location",
                            style={
                                'height':15,
                                "margin-left":"10px",
                                "color":'black',
                                "fontSize": 20
                            },
                        ),
                    ],
                    className="pretty_container four columns",
                ),
                html.Div(
                    [
                        html.H4(
                            "3Is Investment Score",
                            className="control_label",
                        ),
                        html.Br(),
                        html.Div(
                            id="company-score",
                            style={
                                'height':15,
                                "margin-left":"40px",
                                "color":'black',
                                "fontSize": 20
                            },
                        ),
                    ],
                    className="pretty_container three columns",
                ),
                html.Div(
                    [
                        html.Br(),
                        html.Button(
                            "Download CSV",
                            id='button-csv'
                        ),
                        dcc.Download(
                            id='download-company-csv'
                        ),
                    ],
                    className="pretty_container one column",
                ),
            ],
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H4(
                            "Company Brief Description",
                            className='control_label',
                        ),
                        html.Br(),
                        html.Span(
                            id="company-descritpion",
                            style={
                                #'width':1200, 
                                'height':15,
                                "margin-left":"10px",
                                "color":'black',
                                "fontSize": 20
                            },
                        ),
                    ],
                    className="pretty_container twelve columns",
                ),
            ],
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H4(
                            "People",
                            className='control_label',
                        ),
                        dcc.Graph(id="people-logo")
                    ],
                    className="pretty_container thirteen columns",
                ),
            ],
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)


# 1. Update the database and ML models
# update crunchbase database
@app.callback(
    Output('update-crunchbase', 'state'),
    [
        Input('update-crunchbase', 'n_clicks'),
    ],
)
def update_crunchbase(n_clicks):
    if n_clicks == 0:
        return 'You might need to update the database before preceed.'
    else:
        target_path = get_path() + file_name
        # bulkdown using api
        bd = BulkDownload(target_path)
        bd.download_unzip()
        # dump the csv data to the mysql database
        dbm = DBMaker(config_file, 'crunchbase')
        dbm.dump_csv()
        print('Upload has completed.')
        # first round processing the data after the EDA
        print('Start to preprocess data after EDA ...')
        dbr = CBRefinary(
            config_file, 'crunchbase', 'crunchbase_sorted', 
            'crunchbase_ml'
            )
        dbr.sort_all_groups()
        # process the data for training machine learning models
        print('Processing data for ML models ...')
        cbm = CBMill(
            config_file, 'crunchbase', 'crunchbase_sorted', 
            'crunchbase_ml'
        )
        cbm.prepare_ml_data()
        print('Congradulations!')
        print('All crunchbase data has been update. Ready for ML.')

@app.callback(
    Output('retrain-models', 'state'),
    [
        Input('retrain-models', 'n_clicks'),
    ],
)
# retrain model after updating data
# currently, there is bug for not working probably during the training.
def update_model(n_clicks):
    if n_clicks == 0:
        return 'Please update the model after you download new data ...'
    else:
        print('Loading data for ML ...')
        X = df_ml[all_features_ml]
        y = make_y(df_ml)
        mt = ModelTraining()
        mt.train_and_validate_model(X, y, 'gbc')

# 2. search company of interests
# # rule-based keywords matching

@app.callback(
    [
        Output("companies", "options"),
        Output('companies', "value"),
    ],
    [
        Input('search-company-submit-val', 'n_clicks'),
        State('keywords-list-tag', 'value'),
        State('keywords-list', 'value'),
    ],
    revent_initial_call=True,
)
def input_text(n_clicks, tag, keywords):
    if not tag or not keywords:
        return
    mld = ModelLoader()
    matcher = mld.load_matcher()
    if tag not in matcher:
        km = KeywordMatcher()
        km.add_matches(tag, keywords)
        print('Search the keywords in the database')
        search_results = km.search(df_ml)
    else:
        search_results = dl.load_search_results()
    print('Calculating the 3Is investiment score')
    model_best = mld.load_best_model()
    scores = pd.Series(
        [x[1] for x in model_best.predict_proba(search_results)]
    )
    search_results['score'] = round(scores * 100, 2)

    company_probs = pd.concat(
        [search_results['uuid'], scores],
        axis=1
    )
    company_probs.columns = ['uuid', 'proba']
    company_probs_rank = company_probs.sort_values(
        by='proba', ascending=False
    )
    company_rank = list(company_probs_rank['uuid'])
    search_results.set_index('uuid', inplace=True)

    ans = search_results.loc[company_rank, :]
    ans.to_csv(get_path() + 'ranked_search_results.csv')
    print('Compnay search results saved!')

    dict_companies = {k:k for k in ans['name']}
    company_options = make_options(dict_companies)
    print(company_options)

    return company_options, company_rank

# @app.callback(
#     Output("model-select", "children"),
#     [
#         Input('models', 'value'),
#     ],
#     prevent_initial_call=True,
# )
# def select_model(algo):
#     return pickle.load(open(model_path + f"model_{algo}.pkl"), 'rb')


@app.callback(
    Output("map-graph", "figure"),
    [Input("companies", "options")],
)
def map_plot(options):
    if options:
        companies = [x['label'] for x in options]
        selection = df_ml[
            df_ml['name'].map(lambda x: x in companies)
        ]
        selection['size'] = [0.5] * selection.shape[0]
        address = get_coords(selection)
        selection['Lat'] = [address[x][0] for x in selection['name']]
        selection['Lon'] = [address[x][1] for x in selection['name']]
        figure = px.scatter_mapbox(
            selection,
            lat='Lat', lon='Lon',
            size='size',
            hover_name="name",
            hover_data=['short_description'],
            color_discrete_sequence=["#e3a700"],
            center={'lat':38.8283, 'lon': -98.5795},
            zoom=3.5, 
            width=1200, 
            height=600)
    # else:
    #     figure = px.scatter_mapbox(
    #         innovhope_gps,
    #         lat='Lat', lon='Lon',
    #         size='size',
    #         hover_name="name",
    #         color_discrete_sequence=["#e3a700"],
    #         center={'lat':38.8283, 'lon': -98.5795},
    #         zoom=3.5, 
    #         width=1200, 
    #         height=600)

    figure.update_layout(
        mapbox_style="open-street-map",
        plot_bgcolor='#232323',
        paper_bgcolor='#232323',
        font_color='#7FDBFF',
        margin=dict(l=0, r=0, t=0, b=0))
    return figure


@app.callback(
    Output("download-company-csv", "data"),
    [Input("button-csv", "n_clicks"),
     State('keywords-list-tag', 'value'),],
    prevent_initial_call=True,
)
def func(n_clicks, text):
    if not text:
        raise PreventUpdate
    text = '_'.join(text.split(' '))
    df = pd.read_csv(get_path() + 'ranked_search_results.csv')
    df = df[
        [
            'uuid', 'name', 'status', 'short_description', 
            'category_groups_list', 'address', 'city','state_code', 
            'country_code', 'postal_code', 'money_raised_usd', 
            'num_funding_rounds', 'total_funding_usd','share_price_usd', 
            'valuation_price_usd', 'angel', 'convertible_note', 
            'corporate_round', 'debt_financing', 'equity_crowdfunding', 
            'grant', 'initial_coin_offering', 'non_equity_assistance', 
            'post_ipo_debt', 'post_ipo_equity', 'post_ipo_secondary', 
            'pre_seed', 'private_equity', 'product_crowdfunding', 
            'secondary_market', 'seed', 'series_a', 'series_b', 
            'series_c', 'series_d', 'series_e', 'series_f', 'series_g',
            'series_h', 'series_i', 'series_j', 'series_unknown', 
            'undisclosed', 'founded_on', 'last_funding_on', 
            'went_public_on', 'score'
        ]
    ]
    return dcc.send_data_frame(
        df.to_csv, f"{text}_ranked_search_results.csv")


@app.callback(
    Output("time-statistics", "figure"),
    [
        Input("time", "value")
    ]
)
# bar_chart
def bar_chart(time):
    data = DataLoader().load_search_results()
    df = pd.to_datetime(data[time]).dt.year
    df = df.value_counts().reset_index()
    df.columns = [time, 'Count']
    df.sort_values(by='Count', ascending=True, inplace=True)
    figure = px.bar(df, x='Count', y=time, orientation='h')
    figure.update_layout(
        xaxis=dict(showgrid=False),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color='black'
    )
    return figure


@app.callback(
    Output("categorical-statistics", "figure"),
    [
        Input("categorical", "value")
    ]
)
# bar_chart
def bar_chart(categorical):
    data = DataLoader().load_search_results()
    df = data[categorical]
    df = df.value_counts().reset_index()
    df.columns = [categorical, 'Count']
    df.sort_values(by='Count', ascending=True, inplace=True)
    figure = px.bar(df, x='Count', y=categorical, orientation='h')
    figure.update_layout(
        xaxis=dict(showgrid=False),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color='black'
    )
    return figure

@app.callback(
    Output("continuous-statistics", "figure"),
    [
        Input("continuous", "value"),
        Input("categorical", "value")
    ]
)
def histo_chart(continuous, categorical):
    data = DataLoader().load_search_results()
    df = data.fillna(0)
    figure = px.histogram(
        df, 
        x=continuous, 
        color=categorical,
        color_discrete_sequence=px.colors.diverging.Temps,
        nbins=20
    )
    figure.update_layout(
        yaxis=dict(showgrid=False),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color='black'
    )
    return figure


@app.callback(
    [
        Output('company-location', 'children'),
        Output('company-score', 'children'),
    ],
    [Input('companies', 'value')],
    prevent_initial_call=True,
)
def write_text(companies):
    if not companies:
        raise PreventUpdate
        #return dash.no_update
    data = DataLoader().load_ranked_search_results()
    columns_location = [
        'address', 'city', 'state_code', 'postal_code', 'country_code'
    ]
    if companies:
        data_company = data[data['name'] == companies]
        location = ', '.join(
            [
                x for y in data_company[columns_location].values
                for x in y
                if x != 'None'
            ]
        )
        score =  data_company['score']
        if  location == 'NaN':
            location = 'Not Avaliable'
        return [location], score
    else:
        return [None], None

@app.callback(
    [
        Output('company-descritpion', 'children'),
        Output('people-logo', 'figure'),
    ],
    [Input('companies', 'value')],
    prevent_initial_call=True,
)
def get_info(companies):
    if not companies:
        raise PreventUpdate
        #return dash.no_update
    if companies:
        data = DataLoader().load_ranked_search_results()
        uuid = data[data['name'] == companies]['uuid'].iloc[0]
        link = api_lookup_part_1 + uuid + api_lookup_part_2
        print(link)
        response = requests.get(link + api_key).json()
        if 'description' in response['properties']:
            description = response['properties']['description']
            description = re.sub('\n', ' ', description)
        else:
            description = None

        people = [
            [
                x['identifier']['value'], x['image_url'], x['linkedin']['value']
            ] 
            for x in response['cards']['founders'][:4]
        ]
        dummy = pd.DataFrame(
            [[2, 2, x[0]] for x in people],
            columns=['x', 'y', 'Founder']
        )
        fig = px.scatter(dummy, x="x", y="y", facet_col="Founder")
        for col, src in enumerate(people):
            fig.add_layout_image(
                row=1,
                col=col+1,
                source=src[1],
                x=2,
                y=2,
                xanchor='center',
                yanchor='middle',
                sizex=2,
                sizey=2
            )
        fig.update_xaxes(visible=False, showticklabels=False)
        fig.update_yaxes(visible=False, showticklabels=False)
        fig.update_layout(paper_bgcolor="rgb(0,0,0,0)")

        return [description], fig
    else:
        return [None], None
