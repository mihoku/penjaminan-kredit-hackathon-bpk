import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import plotly.graph_objects as go
import plotly.express as px
#import pyodbc
import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
ASSETS_PATH = PATH.joinpath("assets").resolve()
STYLES_PATH = ASSETS_PATH.joinpath("styles").resolve()
MODEL_PATH = PATH.joinpath("data-model").resolve()
DATA_PATH = PATH.joinpath("data-source").resolve()

layouts1 = dcc.Tab(label='Informasi Umum', children=[
    dbc.Jumbotron(
        [
            html.H1("Jumbotron", className="display-3"),
            html.P(
                "Use a jumbotron to call attention to "
                "featured content or information.",
                className="lead",
            ),
            html.Hr(className="my-2"),
            html.P(
                "Jumbotrons use utility classes for typography and "
                "spacing to suit the larger container."
            ),
            html.P(dbc.Button("Learn more", color="primary"), className="lead"),
        ]
    ),

    dbc.Row(
        [
            dbc.Col(html.Div(
                html.Div([
                    html.H5("Latar Belakang", style={"font-weight": "bold"}),
                    html.P("Dalam rangka mendukung kebijakan keuangan negara untuk penanganan pandemi Covid-19 dan pemulihan ekonomi nasional, Pemerintah melalui Peraturan Pemerintah nomor 43 tahun 2020 telah mengatur 4 (empat) modalitas untuk program pemulihan ekonomi nasional (PEN) yang meliputi penyertaan modal negara, penempatan dana, investasi pemerintah, dan penjaminan."),
                    html.P("Pada kegiatan penjaminan kredit modal kerja UMKM, pemerintah menugaskan BUMN dalam hal ini PT Jamkrindo dan PT Askrindo untuk bertindak sebagai penjamin bagi kredit modal kerja Usaha Mikro Kecil Menengah (UMKM). Program penjaminan ini sendiri bertujuan untuk meningkatkan minat perbankan dalam menyalurkan kredit kepada pelaku usaha agar mendapat kemudahan penjaminan saat mengajukan kredit. Selain itu, pemberian modal kerja pada UMKM penting dilakukan dalam membuat kegiatan usaha kembali menggeliat setelah terpuruk akibat dampak pandemi Covid-19."),
                    html.P("Pemerintah telah melakukan berbagai dukungan agar program penjaminan berjalan dengan baik. Pada tahun 2020, pemerintah telah menganggarkan sejumlah Rp6 T untuk memberikan dukungan pada program penjaminan pelaku usaha UMKM dengan rincian Rp5 T sebagai Subsidi Belanja IJP dan Rp1 T untuk dukungan penjaminan loss limit."),
                    html.P("Salah satu dukungan yang dilakukan pemerintah adalah membayarkan seluruh Imbal Jasa Penjaminan (IJP) yang seharusnya ditanggung oleh pelaku usaha sebagai kreditur. IJP yang dianggarkan pemerintah akan dibayarkan ke pihak penjamin sesuai dengan perhitungan yang telah ditetapkan. Salah satu faktor penentuan besaran IJP adalah adanya proyeksi non performing loan (NPL). Penentuan besaran rasio NPL yang akurat akan berpengaruh pada ketepatan jumlah penganggaran yang dilakukan pemerintah dalam alokasi pembayaran IJP. Pada penjaminan pemerintah pada pelaku usaha UMKM, penentuan tarif IJP didasari pada hasil metode perhitungan dan analisa PT Reindonesia Indonesia Utama (RIU) dengan mempertimbangkan proyeksi NPL.")
                ],
                    className="pretty_container")
            ), md=8),
            dbc.Col(html.Div(
                html.Div([
                    html.H5("Tujuan", style={"font-weight": "bold"}),
                    html.Div([
                        html.P(
                            "Melihat sektor usaha UMKM yang paling terdampak dengan adanya pandemi COVID-19", style={"color": "#fff"})
                    ], className="pretty_container",
                        style={"background-color": "#007bff"}),
                    html.Div([
                        html.P("Memberikan usulan tarif IJP yang akan diberikan kepada Jamkrindo dan Askrindo sebagai lembaga penjamin program PEN", style={
                               "color": "#fff"})
                    ], className="pretty_container",
                        style={"background-color": "#28a745"}),
                    html.Div([
                        html.P("Memberikan usulan anggaran belanja subsidi IJP dan Loss Limit yang sesuai dan tepat", style={
                               "color": "#000"})
                    ], className="pretty_container",
                        style={"background-color": "#ffc107"}),
                    html.P("Selain tujuan yang disebutkan di atas, analisis ini juga dapat bermanfaat untuk pelaksanaan kegiatan pengawasan yang dilakukan oleh Inspektorat Jenderal atas penjaminan program PEN. Hasil analisis dapat digunakan untuk melihat apakah tarif yang diusulkan oleh PT Reasuransi Indonesia Utama (PT RIU) telah disusun menggunakan prediksi NPL yang tepat dan anggaran yang diusulkan Direktorat Jenderal Pengelolaan Pembiayaan dan Risiko (DJPPR) sudah tepat.")
                ],
                    id="predictiveDescription",
                    className="pretty_container")
            ), md=4),
        ]
    ),

])
