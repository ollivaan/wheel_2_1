
import pandas as pd
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import math


values_birds_migration_route = []
values_sea_and_archipelago_birds = []
values_mussels = []
values_fish = []


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)
server = app.server

def sundata():
    df_characters = pd.read_csv("data/character_data.csv")
    df_parent = pd.read_csv("data/parent_data.csv")
    
    parent_values = list(df_parent["parent"])
    core_values = list(df_characters["Inner circle"].dropna())
    environment_ecology = list(df_characters["Environment & Ecology"].dropna())
    economy_technology = list(df_characters["Economy & Technology"].dropna())
    social_values = list(df_characters["Social"].dropna())
    species_values = list(df_characters["Species"].dropna())

    parent=[""]+parent_values
    character= core_values+environment_ecology+economy_technology+social_values+species_values

    values = [values_birds_migration_route[-1],values_sea_and_archipelago_birds[-1],values_mussels[-1],values_fish[-1]]

    last_four = []
    species_color = round(sum(values)/4)
    five_values = values
    five_values.append(species_color)

    print(five_values, " FIVE VALUS")
    for num in five_values:
        if num == 0:
            last_four.append("lightgrey")
        elif num == 1:
            last_four.append("red")
        elif num == 2:
            last_four.append("orange")
        elif num == 3:
            last_four.append("yellow")
        elif num == 4:
            last_four.append("lightgreen")
        elif num == 5:
            last_four.append("green")
    
    species_color = [last_four[-1]]
    last_four = last_four[0:4]

    colors_d = {"line": {"width":3},"colors":['lightgrey']*7+species_color+['lightgrey']*42+last_four}
    fig = go.Sunburst(
        labels=character,
        parents=parent,
        opacity=0.8,
        textfont = {'size': 15},
        insidetextorientation = 'horizontal',
        marker = colors_d,
        )
    layout = go.Layout(hovermode='closest', height=1300, width=1300,margin=go.layout.Margin(t=250, l=250, r=250, b=250))
    values.clear()
    return {'data': [fig], 'layout': layout} 

def draw_sunburts_fig():
    fig = sundata()
    app.layout = html.Div(children=[dcc.Graph(figure=fig),],id='dash-container')
    return app.layout



app.layout = html.Div([
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='Tab one', value='tab-1'),
        dcc.Tab(label='Tab two', value='tab-2'),
    ]),
    html.Div(id='tabs-example-content')
])

@app.callback(Output('tabs-example-content', 'children'),
              Input('tabs-example', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([dcc.Input(id="Birds migration routes", type="number",placeholder="Birds migration routes",min=0, max=5, step=1,value=0,)
        ,dcc.Input(id="Sea and archipelago birds", type="number", placeholder="Sea and archipelago birds",min=0, max=5, step=1,value=0,)
        ,dcc.Input(id="Mussels", type="number", placeholder="Mussels",min=0, max=5, step=1,value=0,)
        ,dcc.Input(id="Fish", type="number", placeholder="Fish",min=0, max=5, step=1, value=0,)
        ,html.Hr(),html.Div(id="number-out"),])
    elif tab == 'tab-2':
        return draw_sunburts_fig()

@app.callback(Output("number-out", "children"),Input("Birds migration routes", "value"),Input("Sea and archipelago birds", "value"),Input("Mussels", "value"),Input("Fish", "value"),)

def number_render(bimigro,seabirds,mussels,fish):
    values_birds_migration_route.extend([bimigro])
    values_sea_and_archipelago_birds.extend([seabirds])
    values_mussels.extend([mussels])
    values_fish.extend([fish])

    return "Birds migration routes:  {}, Sea and archipelago birds: {}, Mussels: {}, Fish: {}".format(bimigro, seabirds,mussels,fish,)


if __name__ == '__main__':
    app.run_server(debug=True,dev_tools_ui=False,dev_tools_props_check=False)