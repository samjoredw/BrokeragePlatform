import dash_bootstrap_components as dbc
from dash import html

navbar = dbc.NavbarSimple(
    brand="STONKS Trading Co.",
    brand_href="/",
    children=[
        dbc.NavItem(dbc.NavLink("Sign In", href="/")),
        dbc.NavItem(dbc.NavLink("Account", href="/account")),
        dbc.NavItem(dbc.NavLink("Securities", href="/securities")),
        dbc.NavItem(dbc.NavLink("Trading", href="/trading")),
        dbc.DropdownMenu(
            children=[
                # dbc.DropdownMenuItem("More pages", header=True),
                # dbc.DropdownMenuItem(
                #     f"{page['name']}, href={page['relative_path']}"
                # )
                # for page in dash.page_registry.values()
                dbc.DropdownMenuItem("Github", href="https://github.com"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),

    ],
    color="green",
    dark=True,
)