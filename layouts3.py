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
import pickle
import pathlib
from controls import monthCode, econSector, sectorColor, sectorTxtColor

#get relative data folder
PATH = pathlib.Path(__file__).parent
ASSETS_PATH = PATH.joinpath("assets").resolve()
STYLES_PATH = ASSETS_PATH.joinpath("styles").resolve()
MODEL_PATH = PATH.joinpath("data-model").resolve()
DATA_PATH = PATH.joinpath("data-source").resolve()

#read dataset
df = pd.read_csv(DATA_PATH.joinpath('dataset-predictive-NPL-UMKM.csv'),low_memory=False)

#import model 
model_rf = pickle.load(open(MODEL_PATH.joinpath("penjaminan_predictive_UMKM_with_birate.sav"), "rb"))

pre_df = df[df.Tahun == 2020]
fil_df = pre_df[pre_df.Bulan=="Jun"]
row_take = fil_df[fil_df.SektorEkonomi==econSector[0]]

#populate average 2019 data
prev_df = df[df.Tahun != 2020]
summavg_df = prev_df.groupby('SektorEkonomi', as_index=False).agg({"percentNPL":"mean"})

avg_2019 = []  
    
for i in np.arange(18):
    taken_df = summavg_df[summavg_df.SektorEkonomi==econSector[i]]
    avg_2019.append(taken_df['percentNPL'].values[0]*100)

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
        ],className="three columns pretty_container", style={'background-color':sectorColor[i]})


layouts3 = dcc.Tab(label='Prediksi',children=[html.Div([
    html.Div([#start of macroeconomic vars
              html.H5("Indikator Makro Ekonomi", style={"font-weight":"bold"}),
                        html.Div([ #row div of macro vars
                            html.Div([ #pertumbuhan ekonomi div start
                                html.H5("Pertumbuhan Ekonomi", style={"font-weight":"bold", "color":"#fff"}),
                                dcc.Input(
                                    id="EconGrowth",
                                    type="number",
                                    value=row_take['EconGrowth'].values[0],
                                    debounce=True
                                    ),
                                ],className="pretty_container three columns",style={"background-color":"#111"}),
                            html.Div([ #inflasi div start
                                html.H5("Tingkat Inflasi", style={"font-weight":"bold", "color":"#fff"}),
                                dcc.Input(
                                    id="Inflasi",
                                    type="number",
                                    value=row_take['Inflasi'].values[0],
                                    debounce=True
                                    ),
                                ],className="pretty_container three columns",style={"background-color":"#111"}),
                            html.Div([ #pengangguran div start
                                html.H5("Tingkat Pengangguran", style={"font-weight":"bold", "color":"#fff"}),
                                dcc.Input(
                                    id="Unemployment",
                                    type="number",
                                    value=row_take['Unemployment'].values[0],
                                    debounce=True
                                    ),
                                ],className="pretty_container three columns",style={"background-color":"#111"}),
                            html.Div([ #birate div start
                                html.H5("BI Rate", style={"font-weight":"bold", "color":"#fff"}),
                                dcc.Input(
                                    id="birate",
                                    type="number",
                                    value=3.75,
                                    debounce=True
                                    ),
                                ],className="pretty_container three columns",style={"background-color":"#111"})
                            ],className="row flex-display") #end of macro vars row div
                        ],className=" twelve columns"),#end of macroeconomic var div
        html.Br(),
        html.Br(),
        html.Div([#start of credit channeling vars
              html.H5("Penyaluran Kredit UMKM", style={"font-weight":"bold"}),
              html.Div(children=[generate_form(i) for i in np.arange(18) #row div of macro vars
                            ],className="row flex-display") #end of macro vars row div
              ],className=" twelve columns"),#end of credit channeling var div
    ], className="row pretty_container")])