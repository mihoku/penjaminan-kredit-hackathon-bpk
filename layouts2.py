import flask
from datetime import datetime, timedelta
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
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
df_npl_tahun = df_raw.groupby(['Tahun']).agg({'NPL':'sum','valueChannel':'sum'}).reset_index()
df_npl_tahun_bulan = df_npl = df_raw.groupby(['Tahun','Bulan']).agg({'NPL':'sum','valueChannel':'sum'}).reset_index()
df_npl_tahun['percentNPL'] = df_npl_tahun.NPL / df_npl_tahun.valueChannel
df_npl_tahun_bulan['percentNPL'] = df_npl_tahun_bulan.NPL / df_npl_tahun_bulan.valueChannel

#form generation function
def generate_form(i):
    prefiltered_df = df[df.Tahun == 2020]
    filtered_df = prefiltered_df[prefiltered_df.Bulan=="Jun"]
    data = filtered_df[filtered_df.SektorEkonomi==econSector[i]]
    return html.Div([
        html.P(econSector[i], style={'color': sectorTxtColor[i], 'font-weight':'bold'}),
        html.P("Penyaluran Kredit", style={'color': sectorTxtColor[i]}),
        dcc.Input(
            id="sector_form_{}".format(str(i)),
            type="number",
            value=data['valueChannel'].values[0]*1000000000,
            debounce=True
        ),
        html.P("Proyeksi NPL", style={'color': sectorTxtColor[i]}),
        html.H1(id ="sector_NPL_{}".format(str(i)) , style={'color': sectorTxtColor[i], 'font-weight':'bold', 'font-size':'44px'}),
        html.P(id="sector_NPL_val_{}".format(i) , style={'color': sectorTxtColor[i]})
        ],className="three columns pretty_container", style={'width': '98%', 'background-color':sectorColor[i]})


layouts2 = dcc.Tab(label='Informasi Umum',children=[html.Div([
    html.Div([
            html.H5("Penyaluran Kredit UMKM",style={"font-weight":"bold"}),
            dcc.RadioItems(
                            id='overview-mode',
                            options=[{'label': i, 'value': i} for i in ['Overall', 'Per Sektor']],
                            value='Overall',
                            labelStyle={'display': 'inline-block'}
                        ),
            dcc.Graph(id='overview_figure',style={'height':600}),
            dcc.Slider(
                        id='year-slider',
                        min=df_raw['Tahun'].min(),
                        max=df_raw['Tahun'].max(),
                        value=2020,
                        marks={str(year): str(year) for year in df_raw['Tahun'].unique()},
                        step=None
                    ),
        ], className="pretty_container twelve columns"),
    ], className="row")])

@app.callback(
    Output('overview_figure', 'figure'),
    [Input('overview-mode', 'value'), Input('year-slider','value')])
def change_figure(fig_mode, fig_year = 0):
    if fig_mode == 'Overall':
        fig_data = df_npl_tahun
    else:
        fig_data = df_npl_tahun_bulan[df_npl_tahun_bulan.Tahun == fig_year]
    fig  = px.bar(fig_data, x='Tahun', y='valueChannel') 
    # fig = go.Figure(data=go.Scatter(x=monthCode, y=filtered_df['percentNPL']*100))

    #chart title and transition
    fig.layout.update({'title': 'Persentase NPL'})
    fig.update_layout(transition_duration=500)

    return fig