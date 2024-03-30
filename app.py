import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
# Define the navigation bar
from navigation import navbar

# Import layout for each page
from pages.account import layout as account_layout
from pages.securities import layout as securities_layout
from pages.trading import layout as trading_layout

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define app layout
app.layout = dbc.Container([
    navbar,
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Define callback to update page content based on URL
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/':
        return html.H1("Welcome to STONKS! This is the home page.")
    elif pathname == '/account':
        return account_layout
    elif pathname == '/securities':
        return securities_layout
    elif pathname == '/trading':
        return trading_layout
    else:
        return html.H1("404 - Page not found.")

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
