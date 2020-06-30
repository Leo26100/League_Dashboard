import dash
import dash_core_components as dcc
import dash_html_components as html

from src import appPickBans, appStandings
from src.app import app

print(dcc.__version__)  # 0.6.0 or above is required

app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


@app.callback(
    dash.dependencies.Output("page-content", "children"),
    [dash.dependencies.Input("url", "pathname")],
)
def display_page(pathname):
    if pathname == "/":
        return appStandings.index_page
    elif pathname == "/apps/pickbans":
        return appPickBans.layout
    else:
        return "404"


if __name__ == "__main__":
    app.run_server(debug=True)
