import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
import sqlalchemy
import base64
from navigation import navbar
from pages.account import layout as account_layout
from pages.securities import layout as securities_layout
from pages.trading import layout as trading_layout

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

FINALDATABASE = 'postgresql://se2584:se2584@35.212.75.104/proj1part2'
try:
    engine = sqlalchemy.create_engine(FINALDATABASE)
    conn = engine.connect()
    connection_status = "Database connection successful."
    conn.close()
except Exception as e:
    connection_status = f"Database connection failed: {str(e)}."

app.layout = html.Div([
    html.Div(connection_status, style={'text-align': 'center'}),
    navbar,
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    html.Div([
        html.Div(style={'flex': '1'}),
        dcc.Loading(children=[html.Div(id='account-dropdown-container')])
    ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '10px'})
])

def get_encoded_image(image_filename):
    with open(image_filename, 'rb') as img_file:
        img = base64.b64encode(img_file.read()).decode('utf-8')
        return img

def fetch_userid():
    with engine.connect() as conn:
        query = sqlalchemy.text("""
            SELECT userid
            FROM "user"
            ORDER BY userid
        """)
        result = conn.execute(query)
        user_ids = [{'label': str(row[0]), 'value': row[0]} for row in result.fetchall()]
    return user_ids


def fetch_accountids(userid):
    with engine.connect() as conn:
        query = sqlalchemy.text("""
            SELECT accountid
            FROM account
            WHERE userid = :userid
        """)
        result = conn.execute(query, {"userid": userid})
        account_ids = [{'label': f"Account ID: {row[0]}", 'value': row[0]} for row in result.fetchall()]
    return account_ids


def display_page(pathname):
    if pathname == '/':
        return html.Div([
            html.H1("Please Sign In:"),
            dcc.Dropdown(
                id='user-dropdown',
                options=fetch_userid(),
                placeholder="Select a user",
                style={'width': '300px', 'margin-top': '10px'}
            ),
            html.Div(id='account-dropdown-container'),
            html.Div([
                html.Img(src='data:image/png;base64,{}'.format(get_encoded_image('stock_image.png')),
                         style={'width': '700px', 'margin-top': '10px', 'display': 'block', 'margin-left': 'auto',
                                'margin-right': 'auto'})
            ])
        ])
    elif pathname == '/securities':
        return securities_layout
    elif pathname == '/trading':
        return trading_layout
    elif pathname == '/account':
        return account_layout
    else:
        return html.H1("404 - Page not found.")


@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def update_page(pathname):
    return display_page(pathname)


@app.callback(
    Output('account-dropdown-container', 'children'),
    [Input('user-dropdown', 'value')]
)
def update_account_dropdown(selected_user):
    if selected_user:
        account_options = fetch_accountids(selected_user)
        dropdown = dcc.Dropdown(
            id='account-dropdown',
            options=account_options,
            placeholder="Select an account",
            style={'width': '300px', 'margin-top': '10px'}
        )
    else:
        dropdown = html.Div()
    return dropdown


if __name__ == '__main__':
    app.run_server(debug=True)
