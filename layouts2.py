import flask
from datetime import datetime, timedelta
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_daq as daq
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pathlib
from controls import monthCode, econSector, sectorColor, sectorTxtColor

from app import app

#get relative data folder
PATH = pathlib.Path(__file__).parent
ASSETS_PATH = PATH.joinpath("assets").resolve()
STYLES_PATH = ASSETS_PATH.joinpath("styles").resolve()
MODEL_PATH = PATH.joinpath("data-model").resolve()
DATA_PATH = PATH.joinpath("data-source").resolve()

#read dataset
df_raw = pd.read_csv(DATA_PATH.joinpath('dataset-NPL-UMKM.csv'),low_memory=False)
df_raw.Bulan = pd.Categorical(df_raw.Bulan, categories=monthCode, ordered=True)



df_npl_tahun = df_raw.groupby(['Tahun']).agg({'NPL':'sum','valueChannel':'sum'}).reset_index()
df_npl_tahun_bulan = df_npl = df_raw.groupby(['Tahun','Bulan']).agg({'NPL':'sum','valueChannel':'sum'}).reset_index()
df_npl_tahun['percentNPL'] = df_npl_tahun.NPL / df_npl_tahun.valueChannel
df_npl_tahun_bulan['percentNPL'] = df_npl_tahun_bulan.NPL / df_npl_tahun_bulan.valueChannel

df_sektor = df_raw.groupby(['SektorEkonomi']).agg({'NPL':'sum','valueChannel':'sum'}).reset_index()
df_sektor['percentNPL'] = df_sektor.NPL / df_sektor.valueChannel

df_bubble = df_raw.groupby(['Tahun','SektorEkonomi']).agg({'NPL':'sum','valueChannel':'sum', 'Bulan':'count'}).reset_index()
df_bubble['percentNPL'] = df_bubble.NPL/df_bubble.valueChannel
df_bubble['meanNPL'] = df_bubble.NPL/df_bubble.Bulan
df_bubble['meanValue'] = df_bubble.valueChannel/df_bubble.Bulan

labels = ['Annually', 'Monthly']

layouts2 = dcc.Tab(label='Visualisasi Data',children=[html.Div([
    html.Div([
            html.H5("Penyaluran Kredit UMKM", style={"font-weight":"bold"}),
            html.H6('Overall',style={'display': 'inline-block'}),
            daq.ToggleSwitch(
                id='mode-toggle',
                value=False,
                style={'display': 'inline-block'}
            ),
            html.H6('Sectoral',style={'display': 'inline-block'}),
            html.Br(),
            html.Div([
            dcc.RadioItems(
                            id='submode-toggle',
                            options=[{'label': labels[i], 'value': i} for i in range(len(labels))],
                            value=0,
                            labelStyle={'display': 'inline-block'},
                        ),
                    ], style= {'display': 'block'}), # <-- This is the line that will be changed by the dropdown callback
            html.Div(id='slider-container',children=[
            dcc.Slider(
                        id='year-slider',
                        min=df_raw['Tahun'].min(),
                        max=df_raw['Tahun'].max(),
                        value=2020,
                        marks={str(year): str(year) for year in df_raw['Tahun'].unique()},
                        step=None
                    ),
            ], style= {'display': 'block'}),
            html.Br(),
            dcc.Graph(id='overview-figure',style={'height':600},
                      config = {'scrollZoom' : False,
                                'displaylogo': False,
                                'modeBarButtonsToRemove' : ["zoomIn2d", "zoomOut2d"]}),
        ], className="pretty_container twelve columns"),
    ], className="row")])

@app.callback(
    Output('overview-figure', 'figure'),
    [Input('mode-toggle','value'),
    Input('submode-toggle', 'value'),
    Input('year-slider','value')])
def change_figure(fig_mode, fig_submode, fig_year = 0):
    scmode = 'lines+markers'
    #filterout data
    if fig_mode:
        if fig_submode == 0:
            fig_data = df_sektor
            x_axis = 'SektorEkonomi'
            scmode = 'markers'
            title = 'Total Credit Channel and NPL per Economic Sectors'
        else:
            fig_data = df_bubble[df_bubble.Tahun == fig_year]
            title = str(fig_year) + ' Average of Credit Channel and NPL per Economic Sectors'

    else:
        if fig_submode == 0:
            fig_data = df_npl_tahun
            x_axis = 'Tahun'
            title = 'Total Credit Channel and NPL Annually'
        else:
            fig_data = df_npl_tahun_bulan[df_npl_tahun_bulan.Tahun == fig_year]
            x_axis = 'Bulan'
            title = 'Total Credit Channel and NPL Monthly on ' + str(fig_year)
            

    if fig_submode == 1 and fig_mode:
        fig = px.scatter(fig_data, x='meanValue', y='meanNPL',size='percentNPL',color='SektorEkonomi', log_x=True, size_max=60)
    else:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        # Add traces
        fig.add_trace(
            go.Bar(
                    y=fig_data['valueChannel'],
                    x=fig_data[x_axis],
                    name='Channel',
                    marker_color='skyblue',   
                )
        )
        fig.add_trace(
            go.Bar(
                    y=fig_data['NPL'],
                    x=fig_data[x_axis],
                    name='NPL',
                    marker_color='blue',
                )
        )
        fig.add_trace(
            go.Scatter(
                    y=fig_data['percentNPL'],
                    x=fig_data[x_axis],
                    name='Percentage',
                    marker_color='red',
                    mode=scmode,
                ),
            secondary_y=True,
        )
        #chart title and transition
        fig.layout.update({'barmode':'overlay',
            'yaxis': dict(
                showspikes=True, # Show spike line for X-axis
                # Format spike
                spikethickness=1,
                spikedash="dot",
                spikecolor="#999999",
                spikemode="across",
            ),
        })

    fig.update_layout(title=title,
    legend=dict(
        yanchor="top",
        y=0.9,
    ),
    xaxis = {'showgrid': False},
    yaxis = {'showgrid': False},
    transition_duration = 500,
    hovermode = 'x'
    )

    return fig

@app.callback(
   Output('slider-container', 'style'),
   [Input('submode-toggle','value')])
def hide_year_slider(submode):
    if submode == 0:
        return {'display': 'none'}
    else:
        return {'display': 'block'}

@app.callback(
   Output('submode-toggle', 'options'),
   [Input('mode-toggle','value')])
def hide_year_slider(mode):
    if mode:
        labels = ['Summarize', 'Trend']
    else:
        labels = ['Annually', 'Monthly']

    return [{'label': labels[i], 'value': i} for i in range(len(labels))]