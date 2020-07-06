import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from src import appPickBans, appStandings
from src.app import app

print(dcc.__version__)  # 0.6.0 or above is required

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dbc.Nav(
            className="navbar navbar-expand-lg navbar-dark bg-primary",
            children=[
                dbc.NavItem(
                    html.Div(
                        [
                            dbc.NavLink(
                                "Main Regions", active=True, href="/", className=""
                            )
                        ],
                        className="navbar-nav mr-auto",
                    )
                ),
                dbc.NavItem(
                    html.Div(
                        [dbc.NavLink("Other Regions", href="/OtherTournaments"),],
                        className="navbar-nav mr-auto",
                    )
                ),
            ],
        ),
        html.Div(id="Pages"),
    ]
)
page_layout1 = html.Div(
    [
        dbc.Tabs(
            className="nav nav-tabs",
            children=[
                dbc.Tab(tab_id="tab-1", label="Tournament Stats",),
                dbc.Tab(tab_id="tab-2", label="Tournament Picks and Bans",),
            ],
            id="tabs",
            active_tab="tab-1",
        ),
        html.Div(id="page-content"),
    ]
)


@app.callback(
    dash.dependencies.Output("page-content", "children"),
    [dash.dependencies.Input("tabs", "active_tab")],
)
def switch_tab(at):
    if at == "tab-1":
        return appStandings.index_page
    elif at == "tab-2":
        return appPickBans.layout
    else:
        return "404"


@app.callback(
    dash.dependencies.Output("Pages", "children"),
    [dash.dependencies.Input("url", "pathname")],
)
def display_page(pathname):
    if pathname == "/":
        return page_layout1
    elif pathname == "/OtherTournaments":
        return "Other Page Here"
    else:
        return "404"


if __name__ == "__main__":
    app.run_server(debug=True)
