import sqlalchemy
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

FINALDATABASE = 'postgresql://se2584:se2584@35.212.75.104/proj1part2'
engine = sqlalchemy.create_engine(FINALDATABASE)

# Create a new Dash app for securities
app = dash.Dash(__name__)

# Define the layout for the securities app
security_layout = html.Div([
    html.H1("Securities Page"),
    html.P("This is the securities page. You can view information about securities here."),
    html.Div([
        dcc.Input(id='ticker-input', type='text', placeholder='Enter ticker symbol...'),
        html.Button('Lookup', id='lookup-button', n_clicks=0)
    ]),
    html.Div(id='security-info-container'),
    dcc.Graph(id='security-price-graph')
])

def fetch_security_info(ticker):
    # Function to fetch security information based on ticker
    query = sqlalchemy.text(f"""
        SELECT securityid FROM security WHERE ticker = '{ticker.lower()}';
    """)
    result = conn.execute(query)
    security_id = result.scalar()
    if security_id:
        query_security_info = sqlalchemy.text(f"""
            WITH currencylookup AS (
                SELECT * FROM currency
            )
            SELECT security.name, security.type, security.ticker, security.hqstreetaddress, 
                   security.sharesoutstanding, security.eps, security.sectors, currencylookup.currencyname
            FROM security
            LEFT JOIN currencylookup ON security.currencyid = currencylookup.currencyid
            WHERE security.securityid = {security_id};
        """)
        result_security_info = conn.execute(query_security_info)
        security_info = result_security_info.fetchone()
        return security_info
    else:
        return None

def fetch_security_prices(security_id):
    query_security_prices = sqlalchemy.text(f"""
        SELECT date, price
        FROM securityprice
        WHERE securityid = {security_id}
        ORDER BY date ASC;
    """)
    result_security_prices = conn.execute(query_security_prices)
    security_prices = result_security_prices.fetchall()
    return security_prices

@app.callback(
    Output('security-info-container', 'children'),
    [Input('lookup-button', 'n_clicks')],
    [dash.dependencies.State('ticker-input', 'value')]
)
def display_security_info(n_clicks, ticker):
    if n_clicks > 0 and ticker:
        security_info = fetch_security_info(ticker)
        if security_info:
            name, type, ticker, address, shares_outstanding, eps, sectors, currency_name = security_info
            security_info_html = html.Div([
                html.H3("Security Information"),
                html.Table([
                    html.Tr([html.Th("Name:"), html.Td(name)]),
                    html.Tr([html.Th("Type:"), html.Td(type)]),
                    html.Tr([html.Th("Ticker:"), html.Td(ticker)]),
                    html.Tr([html.Th("HQ Address:"), html.Td(address)]),
                    html.Tr([html.Th("Shares Outstanding:"), html.Td(shares_outstanding)]),
                    html.Tr([html.Th("EPS:"), html.Td(eps)]),
                    html.Tr([html.Th("Sectors:"), html.Td(sectors)]),
                    html.Tr([html.Th("Currency:"), html.Td(currency_name)]),
                ])
            ])
        else:
            security_info_html = html.P("Security not found.")
        return security_info_html
    else:
        return html.Div()

@app.callback(
    Output('security-price-graph', 'figure'),
    [Input('lookup-button', 'n_clicks')],
    [dash.dependencies.State('ticker-input', 'value')]
)
def update_security_price_graph(n_clicks, ticker):
    graph_figure = {'data': [], 'layout': {}}
    if n_clicks > 0 and ticker:
        security_info = fetch_security_info(ticker)
        if security_info:
            security_id = security_info[0]
            security_prices = fetch_security_prices(security_id)
            if security_prices:
                dates = [row[0] for row in security_prices]
                prices = [row[1] for row in security_prices]
                graph_figure = {
                    'data': [
                        {'x': dates, 'y': prices, 'type': 'line', 'name': 'Price'}
                    ],
                    'layout': {
                        'title': 'Security Prices Over Time',
                        'xaxis': {'title': 'Date'},
                        'yaxis': {'title': 'Price'}
                    }
                }
    return graph_figure

if __name__ == '__main__':
    app.run_server(debug=True)
