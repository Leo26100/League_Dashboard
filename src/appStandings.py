import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as tb
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

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
    "GoldDifference",
    "KillsDifference",
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
        html.Br(),
        html.Div(id="region-table"),
        html.Br(),
        html.Div(
            [
                dcc.Dropdown(
                    id="axis",
                    options=[{"label": i, "value": i} for i in graphHeaders],
                    value="Won",
                )
            ]
        ),
        html.Br(),
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
    # standingsData_layout = standingsData_layout.drop(columns=["Tournament"])
    standingsData_layout = (
        standingsData_layout.groupby(["Team"])
        .mean()
        .reset_index()
        .sort_values(by=["Won", "GoldDifference"], ascending=[False, False])
        .round(2)
    )
    standingsData_layout["Standings"] = standingsData_layout["Won"].rank(
        ascending=0, method="first"
    )
    data = standingsData_layout.to_dict("records")
    columns = [{"name": i, "id": i} for i in (standingsData_layout.columns)]
    return (
        html.H1(tournament_title),
        tb.DataTable(
            data=data,
            columns=columns,
            sort_action="native",
            style_cell={"textAlign": "right"},
            style_cell_conditional=[{"if": {"column_id": "Team"}, "textAlign": "left"}],
            style_data_conditional=[
                {
                    "if": {"row_index": "odd"},
                    "background": "rgb(248,248,248)",
                    "fontWeight": "bold",
                },
                {
                    "if": {"filter_query": "{Won} < 0.5", "column_id": "Won"},
                    "backgroundColor": "tomato",
                    "color": "back",
                },
            ],
            style_header={
                "backgroundColor": "rgb(230, 230, 230)",
                "fontWeight": "bold",
            },
        ),
    )


@app.callback(
    dash.dependencies.Output("region-graph", "figure"),
    [
        dash.dependencies.Input("region", "value"),
        dash.dependencies.Input("axis", "value"),
    ],
)
def update_graph_output(region, axis):
    standingsDataGraph = standingsData[region]
    standingsDataGraph = standingsDataGraph.groupby(["Team"]).mean().round(2)
    standingsDataGraphTeam1 = standingsDataGraph.sort_values(by="Won", ascending=False)
    standingsDataGraphTeam1["Standings"] = standingsDataGraphTeam1["Won"].rank(
        ascending=0, method="first"
    )
    standingsDataGraphTeam1 = standingsDataGraphTeam1[
        standingsDataGraphTeam1.Standings.eq(1)
    ]
    fig = px.scatter(
        standingsDataGraph,
        y=standingsDataGraph["Won"],
        x=standingsDataGraph[axis],
        color=list(standingsDataGraph.index.values),
    )
    fig.update_traces(marker_size=30)
    # fig = go.Figure(
    #     data=[
    #         go.Scatter(
    #             name="Team",
    #             y=standingsDataGraph["Won"],
    #             x=standingsDataGraph[axis],
    #             mode="markers",
    #             marker=dict(color=list(standingsDataGraph.index.values),),
    #         ),
    #     ],
    #     layout_title_text='Average "{}"'.format(axis),
    # )

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
