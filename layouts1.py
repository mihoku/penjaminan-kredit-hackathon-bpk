import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import plotly.graph_objects as go
import plotly.express as px
#import pyodbc 
import pandas as pd
import pathlib

#get relative data folder
PATH = pathlib.Path(__file__).parent
ASSETS_PATH = PATH.joinpath("assets").resolve()
STYLES_PATH = ASSETS_PATH.joinpath("styles").resolve()
MODEL_PATH = PATH.joinpath("data-model").resolve()
DATA_PATH = PATH.joinpath("data-source").resolve()

layouts1 = dcc.Tab(label='Informasi Umum',children=[html.Div([
    html.Div([
            html.H5("Informasi Umum",style={"font-weight":"bold"}),

        ], className="pretty_container twelve columns"),
    ], className="row")])

