import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as tb
import pandas as pd
import plotly.graph_objects as go

from src import leaguepediaTable
from src.app import app

dataBaseConnector = leaguepediaTable.dataBaseConnector()
standingsData = dataBaseConnector.scoreBoardTable()
graphHeaders = [
    "Barons",
    "Dragons",
    "Gamelength Number",
    "Gold",
    "Inhibitors",
    "Kills",
    "RiftHeralds",
    "Towers",
]
pickBansData = dataBaseConnector.pickAndBansTable()

index_page = html.Div(
    [
        html.Div(
            [
                html.Label("Region :"),
                dcc.Dropdown(
                    id="region",
                    options=[
                        {"label": r, "value": r}
                        for r in sorted(list(standingsData.keys()))
                    ],
                    value="LCS 2020 Summer",
                ),
            ]
        ),
        html.Div(id="region-table"),
        html.Div(
            [
                dcc.Dropdown(
                    id="axis",
                    options=[{"label": i, "value": i} for i in graphHeaders],
                    value="Gold",
                )
            ]
        ),
        dcc.Graph(id="region-graph"),
        html.Br(),
        html.Div(id="pickbans"),
    ]
)


@app.callback(
    dash.dependencies.Output("region-table", "children"),
    [dash.dependencies.Input("region", "value")],
)
def update_table_output(region):
    standingsData_layout = standingsData[region]
    tournament_title = standingsData_layout["Tournament"][0]
    standingsData_layout = standingsData_layout.drop(columns=["Tournament"])
    data = standingsData_layout.to_dict("records")
    columns = [{"name": i, "id": i} for i in (standingsData_layout.columns)]
    return (html.H1(tournament_title), tb.DataTable(data=data, columns=columns))


@app.callback(
    dash.dependencies.Output("region-graph", "figure"),
    [
        dash.dependencies.Input("region", "value"),
        dash.dependencies.Input("axis", "value"),
    ],
)
def update_graph_output(region, axis):
    standingsDataGraph = standingsData[region]
    standingsDataGraph = standingsDataGraph.groupby(["Team"]).mean()
    fig = go.Figure(
        data=[go.Bar(y=standingsDataGraph[axis], x=standingsDataGraph.index.values)],
        layout_title_text='Average "{}"'.format(axis),
    )
    return fig


@app.callback(
    dash.dependencies.Output("pickbans", "children"),
    [dash.dependencies.Input("region", "value")],
)
def update_pick_bans(region):
    pickBansTable = pickBansData[region]
    data = pickBansTable.to_dict("records")
    columns = [{"name": i, "id": i} for i in (pickBansTable.columns)]
    return tb.DataTable(data=data, columns=columns)


if __name__ == "__main__":
    app.run_server(debug=True)
