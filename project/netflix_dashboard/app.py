import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
from components.navbar import Navbar
from pages import overview, analysis_deep_dive
from data_loader import GLOBAL_DF

# Initialize the Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    suppress_callback_exceptions=True,
)
server = app.server

app.title = "Netflix EDA Dashboard"

navbar_component = Navbar()
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        navbar_component,
        dbc.Container(id="page-content", fluid=True),
    ]
)


# Callback to update page content based on URL
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    print(f"--- app.py: display_page CALLBACK TRIGGERED ---")
    print(f"--- app.py: Current pathname: {pathname}, Type: {type(pathname)} ---")

    if GLOBAL_DF is None:
        print(
            "--- app.py: display_page: GLOBAL_DF is None. Returning error message. ---"
        )
        return dbc.Container(
            [
                html.H1("Error Loading Data", className="text-danger"),
                html.P(
                    "The Netflix dataset could not be loaded. Please check the file path in data_loader.py and ensure the file exists OR there was an import error."
                ),
            ]
        )

    # Handle specific paths
    if pathname == "/analysis-deep-dive":
        print("--- app.py: display_page: Routing to Analysis Deep Dive page. ---")
        try:
            return analysis_deep_dive.layout()
        except Exception as e:
            print(f"--- app.py: ERROR in analysis_deep_dive.layout(): {e} ---")
            return html.Pre(f"Error rendering Analysis Deep Dive page: {e}")
    elif pathname == "/overview":
        print("--- app.py: display_page: Routing to Overview page. ---")
        try:
            return overview.layout()
        except Exception as e:
            print(f"--- app.py: ERROR in overview.layout(): {e} ---")
            return html.Pre(f"Error rendering Overview page: {e}")
    # Handle base path or initial load (pathname can be None initially)
    elif pathname == "/" or pathname is None:
        print(
            f"--- app.py: display_page: Pathname is '{pathname}'. Routing to default Overview page. ---"
        )
        try:
            return overview.layout()
        except Exception as e:
            print(f"--- app.py: ERROR in overview.layout() for default route: {e} ---")
            return html.Pre(f"Error rendering default Overview page: {e}")
    else:
        print(
            f"--- app.py: display_page: Pathname '{pathname}' not recognized. Returning 404. ---"
        )
        return html.Div(
            [
                html.H1("404: Page Not Found", className="text-center"),
                html.P(
                    f"The pathname '{pathname}' was not recognised.",
                    className="text-center",
                ),
            ],
            style={"padding": "20px"},
        )


print("--- app.py: display_page callback defined ---")

if __name__ == "__main__":
    print("--- app.py: Entered __main__ block ---")
    if GLOBAL_DF is not None:
        print(
            "--- app.py: __main__: GLOBAL_DF seems loaded. Attempting to start Dash server... ---"
        )
        app.run(debug=True, port=8051)
    else:
        print(
            "--- app.py: __main__: GLOBAL_DF is None. Dash server will probably not work correctly or display data error. ---"
        )
        # Still try to run the server to see the error message from display_page if GLOBAL_DF is None
        app.run(debug=True, port=8051)
else:
    print("--- app.py: Not in __main__ block (e.g., when imported by Gunicorn) ---")

print("--- app.py: Script execution finished or server started ---")
