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

# # # Initialize the Dash app
# # app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# #
# # app.layout = html.Div(
# #     html.H1(children="STONK Trading Co.")
# # )
# #
# # if __name__ == '__main__':
# #     app.run_server(debug=True)
#
# import base64
# import dash
# from dash import html, dcc
# import dash_bootstrap_components as dbc
# from dash.dependencies import Input, Output
# import sqlalchemy
#
# # Define the navigation bar
# from navigation import navbar
#
# # Import layout for each page
# from pages.account import layout as account_layout
# from pages.securities import layout as securities_layout
# from pages.trading import layout as trading_layout
#
# # Initialize the Dash app
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#
# def display_page(pathname):
#     if pathname == '/':
#         return html.Div([
#             html.H1("Hello"),
#         ])
#     elif pathname == '/securities':
#         return securities_layout
#     elif pathname == '/trading':
#         return trading_layout
#     else:
#         return html.H1("404 - Page not found.")
#
# # Define app layout
# app.layout = html.Div([
#     navbar,
#     dcc.Location(id='url', refresh=False),
#     html.Div(id='page-content'),
#     html.Div([
#         html.Div(style={'flex': '1'}),
#     ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '10px'})
# ])
#
# # Callback to update page content based on URL
# @app.callback(
#     Output('page-content', 'children'),
#     [Input('url', 'pathname')]
# )
# def update_page(pathname):
#     return display_page(pathname)
#
# # Run the app
# if __name__ == '__main__':
#     app.run_server(debug=True)

import base64
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import sqlalchemy

DB_URI = 'postgresql://se2584:se2584@35.212.75.104/proj1part2'
engine = sqlalchemy.create_engine(DB_URI)


def fetch_account_ids():
    with engine.connect() as conn:
        query = sqlalchemy.text("SELECT accountid FROM account")
        result = conn.execute(query)
        account_ids = [row[0] for row in result.fetchall()]
    return sorted(account_ids)


try:
    engine = sqlalchemy.create_engine(DB_URI)
    conn = engine.connect()
    connection_status = "Database connection successful."
    conn.close()
except Exception as e:
    connection_status = f"Database connection failed: {str(e)}"

# Getting account options for sign in
sign_in_options = [{'label': acc_id, 'value': acc_id} for acc_id in fetch_account_ids()]

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


def display_page(pathname):
    if pathname == '/':
        return html.Div([
            html.H1("Welcome back!"),
            dcc.Dropdown(
                id='account-dropdown',
                options=sign_in_options,
                placeholder="Select an account",
                style={'width': '300px', 'margin-top': '10px'}
            )
        ])
    elif pathname == '/securities':
        return securities_layout
    elif pathname == '/trading':
        return trading_layout
    else:
        return html.H1("404 - Page not found.")


# Define app layout
app.layout = html.Div([
    html.Div(connection_status, style={'text-align': 'center'}),  # Center horizontally
    navbar,
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    html.Div([
        html.Div(style={'flex': '1'}),
    ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '10px'})
])


# Callback to update page content based on URL
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def update_page(pathname):
    return display_page(pathname)


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
