#!/usr/bin/env python3

import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, dcc, html, State
from alive_progress import alive_bar


from app import app


layout = html.Div(
    [
        html.H3(
            'Intelligence Crawler', 
            style={"margin-bottom": "35px"}
        ),
        html.H4(
            'Adding New Data to the Database'
        ),
        dcc.Upload(
            [
                'Drag and Drop or ', 
                html.A('Select a csv File')
            ], 
            style={
                "width":"500px", 
                "height":"60px",
                "lineHeight":"60px",
                "borderWidth":"1px",
                "borderStyle":"dashed",
                "boarderRadius":"5px",
                "textAlign":"center",
                "margin-bottom": "40px"
            },
            multiple=False,
        ),
        html.H5("File List"),
        html.Ul(id='file-list', style={"margin-bottom": "35px"}),
        html.H4('Scrapying Company Patents'),
        html.P(
            'Based on the companies listed in crunchbase \
            using US Patent and Trademark website.'
        ),
        html.P(
            'Please select the range of the companies listed \
            in the database.'
        ),
        html.Div(
            [
                dcc.Input(
                    id='patent-start-num', 
                    type='number', 
                    value=None, 
                    style={"margin-right":"10px"}
                ),
                dcc.Input(
                    id='patent-end-num', 
                    type='number', 
                    value=None, 
                    style={"margin-right":"10px"}
                ),
                html.Button(
                    'Start', 
                    id='patent-submit-val', 
                    n_clicks=0
                ),
                html.Div(
                    id='patent-button', 
                    children='Patent crawling is pending.'
                ),
            ], 
            style={"margin-bottom": "40px"}
        ),
        html.H4('Crawling Patent Abstracts'),
        html.P(
            'Based on the Patents numbers crawled from previous step.'
        ),
        html.P(
            'Please select the range of the patent data. \
            Then click Start'
        ),
        html.Div(
            [
                dcc.Input(
                    id='abstract-start-num', 
                    type='number', 
                    value=None, 
                    style={"margin-right":"10px"}
                ),
                dcc.Input(
                    id='abstract-end-num', 
                    type='number', 
                    value=None, 
                    style={"margin-right":"10px"}
                ),
                html.Button(
                    'Start', 
                    id='abstract-submit-val', 
                    n_clicks=0
                ),
                html.Div(
                    id='abstract-button',
                    children='Abstract crawling is pending.'
                ),
            ], 
            style={"margin-bottom": "40px"}
        ),
        html.H4('Crawling Company News'),
        html.P(
            'Based on the company names listed in the database \
            using CNBC news website.'
        ),
        html.P(
            'Please select the range of the companies \
            listed in the database'
        ),
        html.Div(
            [
                dcc.Input(
                    id='news-start-num', 
                    type='number', 
                    value=None, 
                    style={"margin-right":"10px"}
                ),
                dcc.Input(
                    id='news-end-num', 
                    type='number', 
                    value=None, 
                    style={"margin-right":"10px"}
                ),
                html.Button(
                    'Start', 
                    id='news-submit-val', 
                    n_clicks=0
                ),
                html.Div(
                    id='news-button', 
                    children='News scrapying is pending.'
                ),
            ],
        ),
    ],
)


@app.callback(
    Output('abstract-button', 'children'),
    Input('abstract-submit-val', 'n_clicks'),
    State('abstract-start-num', 'value'),
    State('abstract-end-num', 'value'),
)
def abstractUpdates(n_clicks, startNum, endNum):
    if type(startNum) == int and type(endNum) == int:
        if startNum < endNum:
            return 'Scrapyg has been started. Please be patience. \
                Thank you.', scrapying(startNum, endNum)
        else:
            return 'Please select the end number bigger \
                than the starting number.'
    else:
        if startNum or endNum:
            return 'Please input appropriate numbers to \
                start the scrapying service.'
