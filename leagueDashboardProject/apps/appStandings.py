import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as tb 
import pandas as pd 
import plotly.graph_objects as go 

from leagueDashboardProject.app import app
from leagueDashboardProject.apps.dataQueries import layoutData

historicalData = layoutData.layoutHistoricalPage()[0]
standingsData = layoutData.layoutStandingsPage()

index_page =  html.Div([
                html.Div([
                        html.Label("Region :"),
                        dcc.Dropdown(
                            id = 'region',
                            options = [{'label':r, 'value':r} for r in sorted(list(standingsData.keys()))],
                            value = 'North America')
                            ]),
                
                html.Div(id = 'region-table'),
                
                html.Div([
                    dcc.Dropdown(
                    id='x-axis',
                    options = [{'label': i, 'value': i} for i in layoutData.layoutHistoricalPage()[1]],
                    value = 'Gold'
                    )
                    ]),

                dcc.Graph(id = 'region-graph'),
])
@app.callback(
    dash.dependencies.Output('region-table','children'),
    [dash.dependencies.Input(component_id='region', component_property='value')]
              )
def update_table_output(region):
    standingsData_layout = standingsData[region]
    tournament_title = standingsData_layout['Event'][0]
    standingsData_layout = standingsData_layout.drop(columns=['Event','UniqueLine'])
    data = standingsData_layout.to_dict('records')
    columns = [{'name': i, 'id': i} for i in(standingsData_layout.columns)]
    return (html.H1(tournament_title),
        tb.DataTable(data = data, columns = columns)
    )
@app.callback(dash.dependencies.Output('region-graph','figure'), 
[dash.dependencies.Input('region', 'value'),
dash.dependencies.Input('x-axis','value')])
def update_graph_output(region,x_axis):
    standings_graph_table = historicalData[region]
    standings_graph_table_average = standings_graph_table.groupby(['Team']).mean()
    standings_graph_table_average = standings_graph_table_average.reset_index()
    fig = go.Figure(
        data = [go.Bar(y =  standings_graph_table_average[x_axis], x = standings_graph_table_average['Team'])],
        layout_title_text = 'Average "{}"'.format(x_axis)
    ) 
    return fig
    

