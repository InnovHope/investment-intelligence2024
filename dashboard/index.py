#!/usr/bin/env python3

from dash import Input, Output, State, dcc, html
import dash_bootstrap_components as dbc

from app import server, app
from src import home

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#232323",
    paper_bgcolor="#232323",
    legend=dict(
        font=dict(size=10, color='#fbf8f8'),
        orientation="h")
    )

dropdown = dbc.DropdownMenu(
    [
        dbc.DropdownMenuItem(
            "Search", href="/home", style={"fontSize": 15}
        ),
        dbc.DropdownMenuItem(
            "News", href="/ml",style={"fontSize": 15}
        ),
        dbc.DropdownMenuItem(
            "Patent", href="/crawler", style={"fontSize": 15}
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    nav=True,
    in_navbar=True,
    label="Navigate",
    style={"fontSize": 20},
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(
                                src=app.get_asset_url("innovhope.png"),
                                style={"height":"100px"},
                            )
                        ),
                        dbc.Col(
                            dbc.NavbarBrand(
                                "InnovHope Investment Intelligence (3Is) System",
                                className="ms-2",
                                style={"fontSize": 20})
                            ),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/home",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler2", n_clicks=0),
            dbc.Collapse(
                dbc.Nav(
                    [dropdown],
                    className="ms-auto",
                    navbar=True
                ),
                id="navbar-collapse2",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color='dark',
    dark=True,
    className="mb-5",
)

# embedding the navigation bar
app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        navbar,
        html.Div(id='page-content')
])


def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)


@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname='/home'):
    if pathname == '/news':
        return news.layout
    elif pathname == '/patent':
        return patent.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server('0.0.0.0', port=3000, debug=True)
