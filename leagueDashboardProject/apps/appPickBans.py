import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as tb 
import pandas as pd 
import plotly.graph_objects as go 

from leagueDashboardProject.app import app
from leagueDashboardProject.apps.dataQueries.layoutData import statsLayoutPage

pickBansTournament = statsLayoutPage()

layout  = html.Div([
            html.Div([
                html.Label('Region :'),
                dcc.Dropdown(
                    id = 'region_pickbans',
                    options = [{'label': r, 'value': r} for r in sorted(list(pickBansTournament.keys()))],
                    value = 'North America'
                )
            ]),
            html.Div(id='region-table_pickbans')
])
@app.callback(
    dash.dependencies.Output('region-table_pickbans','children'),
    [dash.dependencies.Input('region_pickbans', 'value')]
)

def update_table (region):
    pickBansTable = pickBansTournament[region]
    data = pickBansTable.to_dict('records')
    columns = [{'name': i, 'id': i} for i in(pickBansTable.columns)]
    return (tb.DataTable(data = data, columns = columns))