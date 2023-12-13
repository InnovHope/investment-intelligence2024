import dash
import dash_auth
import dash_bootstrap_components as dbc

VALID_USERNAME_PASSWORD_PAIRS = {
    'innovhope': '3is'
}

external_stylesheets = [dbc.themes.LUX]

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

server = app.server
app.config.suppress_callback_exceptions = True