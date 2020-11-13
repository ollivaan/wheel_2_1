
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

app = dash.Dash(__name__)
server = app.server

def sundata():
    df_characters = pd.read_csv("data/character_data.csv")
    df_parent = pd.read_csv("data/parent_data.csv")
    
    parent_values = list(df_parent["parent"])
    core_values = list(df_characters["Inner circle"].dropna())
    environment_ecology = list(df_characters["Environment & Ecology"].dropna())
    economy_technology = list(df_characters["Economy & Technology"].dropna())
    social_values = list(df_characters["Social"].dropna())

    parent=[""]+parent_values
    character= core_values+environment_ecology+economy_technology+social_values

    fig = go.Sunburst(
        labels=character,
        parents=parent,
        opacity=0.8,
        textfont = {'size': 15},
        insidetextorientation = 'horizontal',
        )
    layout = go.Layout(hovermode='closest', height=1300, width=1300,margin=go.layout.Margin(t=250, l=250, r=250, b=250))
    
    return {'data': [fig], 'layout': layout} 

app = dash.Dash(__name__)
server = app.server
fig = sundata()

app.layout = html.Div(children=[dcc.Graph(figure=fig),],id='dash-container')


@app.callback(
    Output('shot-dist-graph', 'figure'),
    [Input('group-select', 'value')]
)

def get_questions():
    return ""


if __name__ == '__main__':
    app.run_server(debug=True,dev_tools_ui=False,dev_tools_props_check=False)