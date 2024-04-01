import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    brand="STONKS Trading Co.",
    brand_href="/",
    children=[
        dbc.NavItem(dbc.NavLink("Securities", href="/securities")),
        dbc.NavItem(dbc.NavLink("Trading", href="/trading")),
        dbc.DropdownMenu(children=[dbc.DropdownMenuItem("Github",
            href="https://github.com/samjoredw/BrokeragePlatform/tree/main")],
            nav=True,
            in_navbar=True,
            label="More",
        ),

    ],
    color="green",
    dark=True,
)