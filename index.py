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

from app import app
from layouts1 import layouts1
from layouts2 import layouts2
from layouts3 import layouts3
import callbacks1
import callbacks2
import callbacks3

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(#start of header div
        [
            html.Div(
                [
                    html.Img(
                        src=app.get_asset_url("logo.png"),
                        id="logo-image",
                        style={
                            "height": "100px",
                            "width": "auto",
                        },
                    ),
                    html.Div(
                        [
                            html.H3(
                                "Penjaminan Kredit UMKM",
                                style={"margin-bottom": "0px", "font-weight":"bold"},
                            ),
                            html.H5(
                                "Predictive Analytics Dashboard", style={"margin-top": "0px"}
                            ),
                            html.Br(),
                        ]
                    )
                ],
                className="twelve columns",
                id="title",
                )
        ],
        id="header",
        className="row flex-display",
        style={"margin-bottom": "25px"},
        ),#end of header div
    html.Div(id='page-content'),
    html.Div([#start of footer div
        html.P("© 2021 - Ade & Rezas (Hackathon BPK RI)", style={"font-weight":"bold"})
        ],className="pretty_container", style={'text-align':'center'}
        )#end of footer div
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return layouts1
    elif pathname == '/page2':
        return layouts2
    elif pathname == '/page3':
        return layouts3
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)