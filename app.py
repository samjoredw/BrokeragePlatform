import base64

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
import sqlalchemy

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

with open('stock_image.png', 'rb') as f:
    image_data = f.read()

# Convert the image to a base64 string
encoded_image = base64.b64encode(image_data).decode()

# Define dropdown options
dropdown_options = [{'label': str(i), 'value': i} for i in range(1, 13)]

# Define app layout
app.layout = dbc.Container([
    navbar,
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    html.Div([
        html.Div(style={'flex': '1'}),  # Fill empty space
        html.Div("Change account here ➡️ ", style={'margin-right': '20px'}),
        dcc.Dropdown(
            id='account-dropdown',
            options=dropdown_options,
            value=None,  # Default value
            style={'float': 'right', 'margin-right': '20px'}
        )
    ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '10px'})
])

# Define callback to update page content based on URL
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/':
        return html.Img(src='data:image/png;base64,{}'.format(encoded_image),
                        style={'display': 'block', 'margin': 'auto', 'width': '50%', 'height': 'auto'})
    elif pathname == '/account':
        return account_layout
    elif pathname == '/securities':
        return securities_layout
    elif pathname == '/trading':
        return trading_layout
    else:
        return html.H1("404 - Page not found.")

# Callback to update account number
@app.callback(
    Output('account-number', 'children'),
    [Input('account-dropdown', 'value')]
)
def update_account_number(selected_account):
    return selected_account

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
