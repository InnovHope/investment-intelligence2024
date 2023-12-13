from dash import Dash, dcc, html, Input, Output, dash_table
import pandas as pd
from dateutil.relativedelta import relativedelta

df = pd.read_csv("Testing Folder/news_search_results.csv")
df = df[['title','title_link','date','keywords']]


app = Dash(__name__)

app.layout = html.Div([
     
    html.H1("Five News Outlets Results"),
    
    html.Div([
        "Keyword: ",
        dcc.Input(id='keyword', value='beyond meat', type='text')
    ]),

    html.Div([ 
        "Date: ",
        dcc.Dropdown(
            id = 'date',
            options = [
                {"label":"3 months", "value":"3 months"},
                {"label":"6 months", "value":"6 months"},
                {"label":"1 year", "value":"1 year"},
                {"label":"2 year", "value":"2 year"},
                {"label":"All", "value":"All"}
            ],
            multi = False,
            value = "All",
            style = {"width":"50%"}
        ),
    ]),

    html.Br(),
    
    dash_table.DataTable(
        id = 'file-table',
        # columns = [{"name": i, "id": i} for i in df.columns],
        # data = df.to_dict('records'),
        style_data={
            'color': 'black',
            'backgroundColor': 'white',
            'fontSize': 15
        },
        style_header={
            'color': 'black',
            'backgroundColor': 'white',
            'fontWeight': 'bold',
            'fontSize': 20
        },
        style_cell={
            'overflow': 'hidden',
            'textOverflow': 'clip',
            'maxWidth': 0,
            # 'height': '200%'
        },
        style_cell_conditional=[
            {
                'if': {'column_id': 'title'},
                'textAlign': 'left',
                'width': '40%'
            },
            {
                'if': {'column_id': 'title_link'},
                'textAlign': 'left',
                'width': '50%'
            },
        ],
        editable = True
    ),

])


@app.callback(
    [Output(component_id='file-table', component_property='data'),
     Output(component_id='file-table', component_property='columns')],
    [Input(component_id='keyword', component_property='value'),
    Input(component_id='date', component_property='value')]
)
def update_table(keyword, option_slctd):
    
    dff = df.copy()
    dff = dff.loc[dff['keywords'] == keyword]
    columns = ['title','title_link','date']
    dff = dff[columns]
    dff['date'] = pd.to_datetime(dff['date']).dt.date
    # dff = dff[:min(50, len(dff))]
    if option_slctd == '3 months':
        dff = dff[dff['date'] > pd.datetime.now().date() + relativedelta(months=-3)]
    elif option_slctd == '6 months':
        dff = dff[dff['date'] > pd.datetime.now().date() + relativedelta(months=-6)]
    elif option_slctd == '1 year':
        dff = dff[dff['date'] > pd.datetime.now().date() + relativedelta(years=-1)]
    elif option_slctd == '2 year':
        dff = dff[dff['date'] > pd.datetime.now().date() + relativedelta(years=-2)]
    dff = dff.sort_values(by = ['date'], ascending=False)

    data = dff.to_dict('records')
    columns = [{"name": i.capitalize(), "id": i} for i in columns]
    
    return data, columns

if __name__ == '__main__':
    app.run_server(debug=True)
