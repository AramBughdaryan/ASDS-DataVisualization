# netflix_dashboard/components/navbar.py
import dash_bootstrap_components as dbc


def Navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Overview", href="/overview")),
            dbc.NavItem(dbc.NavLink("Analysis Deep Dive", href="/analysis-deep-dive")),
        ],
        brand="Netflix Content Dashboard",
        brand_href="/overview",  # Default page
        color="primary",
        dark=True,
        sticky="top",
        className="mb-4",
    )
    return navbar
