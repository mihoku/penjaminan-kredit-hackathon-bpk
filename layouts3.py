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
        ],className="three columns pretty_container", style={'width': '98%', 'background-color':sectorColor[i]})


layouts3 = dcc.Tab(label='Prediksi',children=[html.Div([
    html.Div([
            html.H5("Analisis Prediktif",style={"font-weight":"bold"}),

        ], className="pretty_container twelve columns"),
    ], className="row")])