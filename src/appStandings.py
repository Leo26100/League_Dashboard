import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table as tb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src import leaguepediaTable
from src.app import app

dataBaseConnector = leaguepediaTable.dataBaseConnector()
standingsData = dataBaseConnector.scoreBoardTable()[0]
graphHeaders = dataBaseConnector.scoreBoardTable()[1]
pickBansData = dataBaseConnector.pickAndBansTable()

index_page = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    md=6,
                    children=[
                        html.Br(),
                        html.H4("Current Main Regions Tournanments:"),
                        html.Br(),
                        dcc.Dropdown(
                            id="region",
                            options=[
                                {"label": r, "value": r}
                                for r in sorted(list(standingsData.keys()))
                            ],
                            value="LCS 2020 Summer",
                        ),
                        html.Br(),
                        html.Div(id="region-table"),
                    ],
                ),
                dbc.Col(
                    md=6,
                    children=[
                        html.Br(),
                        html.H4("Tournament Stats Graphs:"),
                        html.Br(),
                        dcc.Dropdown(
                            id="axis",
                            options=[{"label": i, "value": i} for i in graphHeaders],
                            value="Team",
                        ),
                        html.Br(),
                        dcc.Graph(id="region-graph"),
                        html.Br(),
                    ],
                ),
            ]
        ),
        dbc.Row(
            dbc.Col([dcc.Graph(id="pickbans"),],)
        ),  # width={"Size": 6, "offset": 3}
    ]
)


@app.callback(
    dash.dependencies.Output("region-table", "children"),
    [dash.dependencies.Input("region", "value")],
)
def update_table_output(region):
    standingsData_layout = standingsData[region]
    tournament_title = (region,)
    standingsData_layout = standingsData_layout[["Rankings", "Team", "Won"]]
    data = standingsData_layout.to_dict("records")
    columns = [{"name": i, "id": i} for i in (standingsData_layout.columns)]
    return (
        html.H1(tournament_title),
        tb.DataTable(
            data=data,
            columns=columns,
            sort_action="native",
            style_cell={"textAlign": "right",},
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
    fig = px.scatter(
        standingsDataGraph,
        y=standingsDataGraph["Won"],
        x=standingsDataGraph[axis],
        color=standingsDataGraph["Team"],
    )
    fig.update_traces(marker_size=30, marker={"opacity": 0.4})
    fig.update_layout(title_text="Average {} per Game".format(axis), title_font_size=30)
    return fig


@app.callback(
    dash.dependencies.Output("pickbans", "figure"),
    [dash.dependencies.Input("region", "value")],
)
def update_pick_bans(region):
    picks_df = pickBansData[region][0]
    bans_df = pickBansData[region][1]
    data = bans_df.to_dict("records")
    columns = [{"name": i, "id": i} for i in (bans_df.columns)]
    # fig = go.Figure(data=[go.Histogram(y=bans_df["Champions"])])
    fig_bans = px.histogram(
        bans_df, y="Champions", color="Picks", hover_data=bans_df.columns,
    )
    fig_picks = px.histogram(
        picks_df, y="Champions", color="Position", hover_data=picks_df.columns,
    )
    return fig_picks  # tb.DataTable(data=data, columns=columns),


if __name__ == "__main__":
    app.run_server(debug=True)
