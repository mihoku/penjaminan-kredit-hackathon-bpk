from app import app
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import plotly.graph_objects as go
import plotly.express as px
# import pyodbc
import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
ASSETS_PATH = PATH.joinpath("assets").resolve()
STYLES_PATH = ASSETS_PATH.joinpath("styles").resolve()
MODEL_PATH = PATH.joinpath("data-model").resolve()
DATA_PATH = PATH.joinpath("data-source").resolve()


layouts1 = dcc.Tab(label='Informasi Umum', children=[

    html.Div(
        html.Div([
            html.H3("Summary", style={"font-weight": "bold", "color": "#fff"}),
            html.H5("Dashboard Kondisi Penyaluran serta Sektor UMKM yang Terdampak COVID & Prediksi nilai Non Performance Loan (NPL), Imbal Jasa Penjaminan (IJP), Loss Limit dan Kebutuhan Anggaran Program Penjaminan Kredit UMKM",
                    style={"color": "#fff"}),

        ],
            className="pretty_container", style={"background-color": "#000099"})),

    dbc.Row(
        [
            dbc.Col(html.Div(
                html.Div([
                    html.H5("Latar Belakang", style={"font-weight": "bold"}),
                    html.P("Dalam rangka mendukung kebijakan keuangan negara untuk penanganan pandemi Covid-19 dan pemulihan ekonomi nasional, Pemerintah melalui Peraturan Pemerintah nomor 43 tahun 2020 telah mengatur 4 (empat) modalitas untuk program pemulihan ekonomi nasional (PEN) yang meliputi penyertaan modal negara, penempatan dana, investasi pemerintah, dan penjaminan."),
                    html.P("Pada kegiatan penjaminan kredit modal kerja UMKM, pemerintah menugaskan BUMN dalam hal ini PT Jamkrindo dan PT Askrindo untuk bertindak sebagai penjamin bagi kredit modal kerja Usaha Mikro Kecil Menengah (UMKM). Salah satu dukungan yang dilakukan pemerintah adalah membayarkan seluruh Imbal Jasa Penjaminan (IJP) yang seharusnya ditanggung oleh pelaku usaha sebagai kreditur. Faktor penentuan besaran IJP adalah adanya proyeksi non performing loan (NPL). Penentuan besaran rasio NPL yang akurat akan berpengaruh pada ketepatan jumlah penganggaran yang dilakukan pemerintah dalam alokasi pembayaran IJP. Pada penjaminan pemerintah pada pelaku usaha UMKM, penentuan tarif IJP didasari pada hasil metode perhitungan dan analisa PT Reindonesia Indonesia Utama (RIU) dengan mempertimbangkan proyeksi NPL."),
                    html.Div([
                        html.Img(
                            src=app.get_asset_url("skema_pen.JPG"),
                            style={
                                "height": "auto",
                                "width": "100%",
                            },
                        ),  # end of logo img tag
                    ], style={'text-align': 'center', 'width': '100%', 'display': 'inline-block'}),

                    html.P("Skema Program PEN Penjaminan Pelaku Usaha UMKM", style={"text-align": "center"})

                ],
                    className="pretty_container")
            ), md=8),
            dbc.Col(html.Div(
                html.Div([
                    html.H5("Fitur Dashboard", style={"font-weight": "bold"}),
                    html.Div([
                        html.P("Visualisasi atas Data Historis Penyaluran serta NPL atas Kredit UMKM",
                               style={"color": "#fff"})
                    ], className="pretty_container",
                        style={"background-color": "#007bff"}),
                    html.Div([
                        html.P("Evaluasi atas Sektor Ekonomi UMKM yang terdampak pandemi",
                               style={"color": "#fff"})
                    ], className="pretty_container",
                        style={"background-color": "#28a745"}),
                    html.Div([
                        html.P("Prediksi IJP dan Loss Limit berdasarkan model",
                               style={"color": "#fff"})
                    ], className="pretty_container",
                        style={"background-color": "#ff8000"}),
                    html.Div([
                        html.P("Prediksi Tarif IJP yang diusulkan oleh PT RIU",
                               style={"color": "#fff"})
                    ], className="pretty_container",
                        style={"background-color": "#ff0040"}),
                    html.H1(" ", style={"font-weight": "bold"}),
                    html.H1(" ", style={"font-weight": "bold"}),
                    html.H1(" ", style={"font-weight": "bold"})
                ],
                    className="pretty_container")
            ), md=4),
        ]
    ),

    html.Div([  # start of credit channeling vars
        html.H5("Manfaat", style={
            "font-weight": "bold", "text-align": "center"}),
        html.Div(children=[
            html.Div([
                html.P("Melihat sektor usaha UMKM yang paling terdampak dengan adanya pandemi COVID-19",
                       style={"color": "#fff", "text-align": "center"}),
            ], className="three columns pretty_container", style={'background-color': '#007bff'}),
            html.Div([
                html.P("Memberikan usulan tarif IJP yang akan diberikan kepada Jamkrindo dan Askrindo sebagai lembaga penjamin program PEN",
                       style={"color": "#fff", "text-align": "center"}),
            ], className="three columns pretty_container", style={'background-color': '#28a745'}),
            html.Div([
                html.P("Memberikan usulan anggaran belanja subsidi IJP dan Loss Limit yang sesuai dan tepat",
                       style={"color": "#fff", "text-align": "center"}),
            ], className="three columns pretty_container", style={'background-color': '#ff8000'}),
            html.Div([
                html.P("Memberikan gambaran umum dalam proses perencanaan pemeriksaan keuangan negara",
                       style={"color": "#fff", "text-align": "center"}),
            ], className="three columns pretty_container", style={'background-color': '#ff0040'}),

            # row div of macro vars
        ], className="row flex-display")  # end of macro vars row div
    ], className="pretty_container", style={"text-align": "center"}),

    html.Div([  # start of model chart
        html.H5("Model Prediktif", style={"font-weight": "bold"}),
        html.Div([
             html.P("Model prediktif ini dikembangkan atas target utama yakni NPL penyaluran kredit kepada UMKM. Terdapat beberapa aspek yang menjadi prediktor dan secara umum terbagi ke dalam dua kelompok besar, yakni kondisi makroekonomi dan sektor ekonomi UMKM."),
             html.P("Algoritma Random Forest Regression digunakan dalam pengembangan model prediktif tersebut. Random Forest merupakan jenis algoritma ensemble yang mengkombinasikan beberapa decision tree untuk membuat prediksi finalnya."),
             html.P("Sumber data yang digunakan dalam pengembangan model prediktif ini adalah Laporan Statistik Perbankan Indonesia dari Otoritas Jasa Keuangan, serta Badan Pusat Statistik untuk indikator makroekonomi.")
             ], style={'width': '40%', 'display': 'inline-block'}),
        html.Div([
            html.Img(
                 src=app.get_asset_url("model-chart.png"),
                 style={
                     "height": "auto",
                     "width": "70%",
                 },
                 ),  # end of logo img tag
        ], style={'text-align': 'center', 'width': '60%', 'display': 'inline-block'}),
    ], className="pretty_container", style={'background-color': '#fff'}),




])
