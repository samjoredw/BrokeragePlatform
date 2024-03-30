import dash_bootstrap_components as dbc
from dash import html

navbar = dbc.NavbarSimple(
    brand="STONKS",
    brand_href="/",
    children=[
        dbc.NavItem(dbc.NavLink("Account", href="/account")),
        dbc.NavItem(dbc.NavLink("Securities", href="/securities")),
        dbc.NavItem(dbc.NavLink("Trading", href="/trading")),
    ],
    color="primary",
    dark=True,
)