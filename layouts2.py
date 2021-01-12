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
df_raw.NPL = df_raw.NPL * (10**9)
df_raw.valueChannel = df_raw.valueChannel * (10**9)


df_npl_tahun = df_raw.groupby(['Tahun']).agg({'NPL':'sum','valueChannel':'sum'}).reset_index()
df_npl_tahun_bulan = df_npl = df_raw.groupby(['Tahun','Bulan']).agg({'NPL':'sum','valueChannel':'sum'}).reset_index()
df_npl_tahun['percentNPL'] = (df_npl_tahun.NPL / df_npl_tahun.valueChannel *100).round(2)
df_npl_tahun_bulan['percentNPL'] = (df_npl_tahun_bulan.NPL / df_npl_tahun_bulan.valueChannel *100).round(2)

df_sektor = df_raw.groupby(['SektorEkonomi']).agg({'NPL':'sum','valueChannel':'sum'}).reset_index()
df_sektor['percentNPL'] = (df_sektor.NPL / df_sektor.valueChannel *100).round(2)

df_bubble = df_raw.groupby(['Tahun','SektorEkonomi']).agg({'NPL':'sum','valueChannel':'sum', 'Bulan':'count'}).reset_index()
df_bubble['percentNPL'] = (df_bubble.NPL/df_bubble.valueChannel*100).round(2)
df_bubble['monthlyNPL'] = df_bubble.NPL/df_bubble.Bulan
df_bubble['monthlyCredit'] = df_bubble.valueChannel/df_bubble.Bulan

layouts2 = dcc.Tab(label='Visualisasi Data',children=[html.Div([
    html.Div([
            # ================= OVERALL GRAPH =====================
            html.H3([html.Center("Overall Non-Performing-Loan on UMKM Credit 2011-2020")], style={"font-weight":"bold"}),
            html.H6('Annually',style={'display': 'inline-block'}),
            daq.ToggleSwitch(
                id='overall-mode-toggle',
                value=False,
                style={'display': 'inline-block'}
            ),
            html.H6('Monthly',style={'display': 'inline-block'}),
            html.Br(),
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
            html.Br(),
            # =============== SECTORAL GRAPH ======================
            html.H3([html.Center("Sectoral Non-Performing-Loan on UMKM Credit 2011-2020")], style={"font-weight":"bold"}),
            html.H6('Summary',style={'display': 'inline-block'}),
            daq.ToggleSwitch(
                id='sectoral-mode-toggle',
                value=False,
                style={'display': 'inline-block'}
            ),
            html.H6('Annual Trend',style={'display': 'inline-block'}),
            html.Br(),
            html.Div(id='dropdown-container',children=[
            html.B('Economic Sector'),
            dcc.Dropdown(
                id='sector-dropdown',
                options=[{'label':i, 'value':i} for i in econSector],
                value=econSector[0]
            ),
            ], style= {'display': 'block'}),
            html.Br(),
            dcc.Graph(id='sectoral-figure',style={'height':600},
                      config = {'scrollZoom' : False,
                                'displaylogo': False,
                                'modeBarButtonsToRemove' : ["zoomIn2d", "zoomOut2d"]}),
        ], className="pretty_container twelve columns"),
    ], className="row")])

#====================== Overall CallBack =========================

@app.callback(
    Output('overview-figure', 'figure'),
    [Input('overall-mode-toggle','value'),
    Input('year-slider','value')])
def change_overall_figure(fig_mode, fig_year = 0):
    if not fig_mode:
        fig_data = df_npl_tahun
        x_axis = 'Tahun'
        title = 'Total Credit Channel and NPL Annually'
    else:
        fig_data = df_npl_tahun_bulan[df_npl_tahun_bulan.Tahun == fig_year]
        x_axis = 'Bulan'
        title = 'Total Credit Channel and NPL Monthly on ' + str(fig_year)
            
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # Add traces
    fig.add_trace(
        go.Bar(
                y=fig_data['valueChannel'],
                x=fig_data[x_axis],
                name='Credit',
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
                name='Percent NPL',
                marker_color='red',
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
   [Input('overall-mode-toggle','value')])
def hide_year_slider(mode):
    if not mode:
        return {'display': 'none'}
    else:
        return {'display': 'block'}

#====================== Sectoral CallBack =========================

@app.callback(
    Output('sectoral-figure', 'figure'),
    [Input('sectoral-mode-toggle','value'),
    Input('sector-dropdown','value')])
def change_sectoral_figure(fig_mode, fig_sector = 0):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    if not fig_mode:
        fig_data = df_sektor
        fig_data = fig_data.sort_values(by='valueChannel', axis=0, ascending=True)
        title = 'Total Credit Channel and NPL per Economic Sectors'

        fig.add_trace(
            go.Bar(
                x=fig_data['valueChannel'],
                y=fig_data['SektorEkonomi'],
                name='Credit',
                marker_color='skyblue',
                orientation = 'h'   
            )
        )
        fig.add_trace(
            go.Bar(
                x=fig_data['NPL'],
                y=fig_data['SektorEkonomi'],
                name='NPL',
                marker_color='blue',
                orientation='h'
            )
        )

        fig.add_trace(
            go.Scatter(
                    x=fig_data['percentNPL'],
                    y=fig_data['SektorEkonomi'],
                    name='Percent NPL',
                    marker_color='red',
                    xaxis= 'x2',
                    mode = 'markers',
                ),
        )

        #chart title and transition
        fig.layout.update({'barmode':'overlay',
            'xaxis':dict(title= 'Credit/NPL value',
                showspikes=True, # Show spike line for X-axis
                # Format spike
                spikethickness=1,
                spikedash="dot",
                spikecolor="#999999",
                spikemode="across",
            ),
            'xaxis2': dict(overlaying= 'x', 
                side= 'top',
                title= 'NPL percentage'),
            'hovermode' : 'y',
        })
    else:
        fig_data = df_bubble[df_bubble.SektorEkonomi == fig_sector]
        title = 'Monthly Average '+str(fig_sector) + ' Credit Channel and NPL per Year'
        
        fig.add_trace(
            go.Bar(
                y=fig_data['monthlyCredit'],
                x=fig_data['Tahun'],
                name='Credit',
                marker_color='skyblue',  
            )
        )
        fig.add_trace(
            go.Bar(
                y=fig_data['monthlyNPL'],
                x=fig_data['Tahun'],
                name='NPL',
                marker_color='blue',
            )
        )

        fig.add_trace(
            go.Scatter(
                    y=fig_data['percentNPL'],
                    x=fig_data['Tahun'],
                    name='Percent NPL',
                    marker_color='red',
                ),secondary_y=True
        )
        
        #chart title and transition
        fig.layout.update({'barmode':'overlay',
            'yaxis':dict(
                showspikes=True, # Show spike line for X-axis
                # Format spike
                spikethickness=1,
                spikedash="dot",
                spikecolor="#999999",
                spikemode="across",
            ),
            'hovermode' : 'x',
        })
    

    fig.update_layout(title=title,
    xaxis = {'showgrid': False},
    yaxis = {'showgrid': False},
    )

    return fig


@app.callback(
   Output('dropdown-container', 'style'),
   [Input('sectoral-mode-toggle','value')])
def hide_sector_dropdown(mode):
    if not mode:
        return {'display': 'none'}
    else:
        return {'display': 'block'}