import base64
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
import sqlalchemy
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


def fetch_userid():
    with engine.connect() as conn:
        query = sqlalchemy.text("""
            SELECT userid
            FROM "user"
            ORDER BY userid
        """)
        result = conn.execute(query)
        user_ids = [{'label': f"User ID: {str(row[0])}", 'value': row[0]} for row in result.fetchall()]
    return user_ids


app.layout = html.Div([
    html.Div(connection_status, style={'text-align': 'center'}),
    navbar,
    dcc.Location(id='url', refresh=False),
    html.H6([
        html.Div("Please Sign In:", style={"margin-top": "10px"}),
        dcc.Dropdown(
            id='user-dropdown',
            options=fetch_userid(),
            placeholder="Select a user",
            style={'width': '300px', 'margin-top': '10px'}
        ),
        html.Div(id='account-dropdown-container'),
    ]),
    html.Div(id='page-content'),
])

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def update_page(pathname):
    if pathname == '/':
        return html.Div([
            html.Div(id='profile-container', style={'float': 'right', 'margin-left': '20px', 'margin-right': '90px'}),
            html.Div([
                html.Div(id='holdings-container',
                         style={'font-size': '14px', "margin-right": "2000px", "margin-left": "40px"}),
                html.Div(id='transactions-container',
                         style={'font-size': '14px', "margin-right": "2000px", "margin-left": "40px"}),
                html.Div(id='transfers-container',
                         style={'font-size': '14px', "margin-right": "2000px", "margin-left": "40px"})
            ]),
            html.Div([
                html.Img(
                    src='data:image/png;base64,{}'.format(get_encoded_image('stock_image.png')),
                    style={'width': '700px', 'margin-top': '10px', 'display': 'block', 'margin-left': 'auto',
                           'margin-right': '80px'}
                )
            ], style={'float': 'left'}),
        ])
    elif pathname == '/securities':
        return securities_layout
    elif pathname == '/trading':
        return trading_layout
    elif pathname == '/account':
        return account_layout
    else:
        return html.H1("404 - Page not found.")


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

def fetch_profile(user_id):
    with engine.connect() as conn:
        query = sqlalchemy.text(f"""
            SELECT
            firstname,
            lastname,
            dateofbirth,
            streetaddress,
            city,
            zip,
            country,
            phonenumber,
            bankaccountrouting,
            bankaccountnumber
            FROM "user"
            WHERE userid = {user_id}
        """)
        result = conn.execute(query)
        profile_data = result.fetchone()
    return profile_data

def fetch_transactions(user_id):
    with engine.connect() as conn:
        query = sqlalchemy.text(f"""
            WITH accountinfo AS (
                SELECT transactionid, securityid, sharecount, price, action, dateinitiated, datecompleted, accountid
                FROM transaction
                WHERE accountid IN (
                    SELECT accountid
                    FROM account
                    WHERE userid = {user_id}
                )
            ), accounttypes AS (
                SELECT accountid, accounttype
                FROM account
                WHERE userid = {user_id}
            ), securityinfo AS (
                SELECT securityid, name
                FROM security
            )
            SELECT accounttypes.accounttype, 
                    accountinfo.accountid, 
                    accountinfo.transactionid, 
                    accountinfo.securityid, 
                    securityinfo.name, 
                    accountinfo.sharecount, 
                    accountinfo.price,
                CASE WHEN accountinfo.action THEN 'BUY'
                ELSE 'SELL'
                END AS buysell, accountinfo.dateinitiated, accountinfo.datecompleted
            FROM accountinfo
            LEFT JOIN accounttypes ON accountinfo.accountid = accounttypes.accountid
            LEFT JOIN securityinfo ON accountinfo.securityid = securityinfo.securityid
            WHERE accountinfo.accountid IN (
                SELECT accountid
                FROM account
                WHERE userid = {user_id}
            )
            ORDER BY accountinfo.datecompleted DESC;
        """)
        result = conn.execute(query)
        transactions_data = result.fetchall()
    return transactions_data


def display_transactions(transactions_data):
    if transactions_data:
        table_rows = [
            html.Tr([
                html.Td(data) for data in row
            ]) for row in transactions_data
        ]
        table = html.Table([
            html.Thead(html.Tr([html.Th(col) for col in
                                ['Account Type', 'Account ID', 'Transaction ID', 'Security ID', 'Security Name',
                                 'Share Count', 'Price', 'Action', 'Date Initiated', 'Date Completed']])),
            html.Tbody(table_rows)
        ], className='table table-striped table-bordered table-hover', style={'font-size': '14px'})

        transactions_html = html.H2("Transactions", style={"font-size": "30px", "margin-bottom": "10px"}), html.Div([table])
    else:
        transactions_html = html.Div()
    return transactions_html


def fetch_transfers(user_id):
    with engine.connect() as conn:
        query = sqlalchemy.text(f"""
            WITH accounttypes AS (
                SELECT accountid, accounttype
                FROM account
                WHERE userid = {user_id}
            )
            SELECT accounttypes.accounttype, transferid, amount, dateinitiated, datecompleted
            FROM transfer
            LEFT JOIN accounttypes ON transfer.accountid = accounttypes.accountid
            WHERE transfer.accountid IN (
                SELECT accountid
                FROM account
                WHERE userid = {user_id}
            )
            ORDER BY datecompleted DESC;
        """)
        result = conn.execute(query)
        transfers_data = result.fetchall()
    return transfers_data


def display_transfers(transfers_data):
    if transfers_data:
        table_rows = [
            html.Tr([
                html.Td(data) for data in row
            ]) for row in transfers_data
        ]
        table = html.Table([
            html.Thead(html.Tr([html.Th(col) for col in
                                ['Account Type', 'Transfer ID', 'Amount', 'Date Initiated', 'Date Completed']])),
            html.Tbody(table_rows)
        ], className='table table-striped table-bordered table-hover', style={'font-size': '14px'})

        transfers_html = html.H2("Transfers", style={"font-size": "30px", "margin-bottom": "10px"}), html.Div([table])
    else:
        transfers_html = html.Div()
    return transfers_html


def display_profile(profile_data):
    if profile_data:
        profile_html = dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H2(
                            "Profile",
                            style={
                                "font-size": "40px",  # Increase text size
                                "text-align": "center",  # Center align the header
                                "font-family": "Arial, sans-serif"  # Apply slick font
                            }
                        ),
                        html.P(f"Name: {profile_data[0]} {profile_data[1]}"),
                        html.P(f"Date of Birth: {profile_data[2]}"),
                        html.P(
                            f"Address: {profile_data[3]}, {profile_data[4]}, {profile_data[5]}, {profile_data[6]}"
                        ),
                        html.P(f"Phone Number: {profile_data[7]}"),
                        html.P(f"Bank Account Routing: {profile_data[8]}"),
                        html.P(f"Bank Account Number: {profile_data[9]}")
                    ]
                )
            ],
            style={
                "borderRadius": "15px",
                "margin-left": "10px",  # Move the box to the left side of the page
                "margin-right": "auto",  # Center the box horizontally
                "background-color": "#c8e6c9",  # Darker green color
                "box-shadow": "5px 5px 5px grey",  # Add shadow for depth
                "width": "fit-content",  # Expand to fit content
                "font-family": "Arial, sans-serif"  # Apply slick font to the box
            }
        )
    else:
        profile_html = html.Div()
    return profile_html


def fetch_holdings(user_id, account_id):
    with engine.connect() as conn:
        query = sqlalchemy.text(f"""
            WITH accounttypes AS (
                SELECT accountid, accounttype
                FROM account
                WHERE userid = {user_id}
            ), securityinfo AS (
                SELECT securityid, name
                FROM security
            )
            SELECT accounttypes.accounttype, securityinfo.name, holding.sharecount, holding.purchaseprice, holding.purchasedate
            FROM holding
            LEFT JOIN accounttypes ON holding.accountid = accounttypes.accountid
            LEFT JOIN securityinfo ON holding.securityid = securityinfo.securityid
            WHERE holding.accountid = {account_id}
        """)
        result = conn.execute(query)
        holdings_data = result.fetchall()
    return holdings_data


def display_holdings(holdings_data):
    if holdings_data:
        table_rows = [
            html.Tr([
                html.Td(data) for data in row
            ]) for row in holdings_data
        ]

        table = html.Table([
            html.Thead(html.Tr([html.Th(col) for col in
                                ['Account Type', 'Name', 'Share Count', 'Purchase Price', 'Purchase Date']])),
            html.Tbody(table_rows)
        ], className='table table-striped table-bordered table-hover', style={'font-size': '14px'})

        holdings_html = html.H2("Holdings", style={"font-size": "30px", "margin-bottom": "10px"}), html.Div([table])
    else:
        holdings_html = html.Div()
    return holdings_html


def get_encoded_image(image_filename):
    with open(image_filename, 'rb') as img_file:
        img = base64.b64encode(img_file.read()).decode('utf-8')
        return img


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

@app.callback(
    Output('profile-container', 'children'),
    [Input('account-dropdown', 'value')]
)
def display_profile_data(account_id):
    if account_id:
        user_id = get_user_id_from_account(account_id)
        if user_id:
            profile_data = fetch_profile(user_id)
            profile_html = display_profile(profile_data)
        else:
            profile_html = html.Div("User not found")
    else:
        profile_html = html.Div("")
    return profile_html

@app.callback(
    Output('holdings-container', 'children'),
    [Input('account-dropdown', 'value'),
     Input('user-dropdown', 'value')]
)
def display_holdings_data(account_id, user_id):
    if account_id and user_id:
        holdings_data = fetch_holdings(user_id, account_id)
        holdings_html = display_holdings(holdings_data)
    else:
        holdings_html = html.Div("")
    return holdings_html


@app.callback(
    Output('transfers-container', 'children'),
    [Input('account-dropdown', 'value'),
     Input('user-dropdown', 'value')]
)
def display_transfers_data(account_id, user_id):
    if account_id and user_id:
        transfers_data = fetch_transfers(user_id)
        transfers_html = display_transfers(transfers_data)
    else:
        transfers_html = html.Div("")
    return transfers_html


@app.callback(
    Output('transactions-container', 'children'),
    [Input('account-dropdown', 'value'),
     Input('user-dropdown', 'value')]
)
def display_transactions_data(account_id, user_id):
    if account_id and user_id:
        transactions_data = fetch_transactions(user_id)
        transactions_html = display_transactions(transactions_data)
    else:
        transactions_html = html.Div("")
    return transactions_html


def get_user_id_from_account(account_id):
    with engine.connect() as conn:
        query = sqlalchemy.text("""
            SELECT userid
            FROM account
            WHERE accountid = :account_id
        """)
        result = conn.execute(query, {"account_id": account_id})
        user_id = result.scalar()
    return user_id

if __name__ == '__main__':
    app.run_server(debug=True)
