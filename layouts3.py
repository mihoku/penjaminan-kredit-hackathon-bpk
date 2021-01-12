import flask
from datetime import datetime, timedelta
import dash
import dash_table
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

from app import app

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

economic_sector = pd.Series(econSector, name='sector')

avg_2019 = []  
    
for i in np.arange(18):
    taken_df = summavg_df[summavg_df.SektorEkonomi==econSector[i]]
    avg_2019.append(taken_df['percentNPL'].values[0]*100)

average_NPL_2019 = pd.Series(avg_2019, name='average_NPL_2019')

df_2019 = pd.concat([economic_sector,average_NPL_2019], axis=1)

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


layouts3 = dcc.Tab(label='Evaluasi Tarif dan Anggaran IJP, serta Sektor Terdampak',children=[html.Div([
    
        html.Div([#start of prediction result
                 html.Div([ #row div of prediction result
                        html.Div([ #start of column div for total SME Credit channeling
                            html.H5("Total Penyaluran Kredit UMKM", style={'font-weight':'bold'}),
                            html.H4(id ="total_credit", style={'font-weight':'bold', 'font-size':'36px'}),
                            ], className="pretty_container five columns",
                            style={'text-align':'center','background-color':'#fff', 'border-top':'6px solid #fd7e14'}
                            ),#end of column div for total SME credit channeling
                        html.Div([ #start of column div for total NPL Projection
                            html.H5("Proyeksi Total NPL Kredit UMKM", style={'font-weight':'bold'}),
                            html.H1(id ="total_NPL", style={'font-weight':'bold', 'font-size':'44px'}),
                            html.P(id="total_NPL_val")
                            ], className="pretty_container six columns",
                            style={'text-align':'center','background-color':'#fff', 'border-top':'6px solid #ffc107'}
                            ),#end of column div for total NPL projection
                        html.Div([ #start of column div for explanation
                            html.P("NPL kredit UMKM diproyeksikan menggunakan 4 (empat) indikator makroekonomi yaitu pertumbuhan ekonomi, tingkat inflasi, tingkat pengangguran, serta suku bunga BI. Selain itu, proyeksi juga didasarkan pada penyaluran kredit kepada masing-masing 18 sektor ekonomi UMKM sebagaimana klasifikasi Otoritas Jasa Keuangan (OJK). Kondisi makroekonomi beserta penyaluran kredit UMKM per sektor tersebut dapat disesuaikan berdasarkan kondisi terkini. Hasil proyeksi atas NPL dapat dipergunakan sebagai alat evaluasi atas penetapan tarif dan anggaran IJP oleh Pemerintah, serta mengevaluasi sektor ekonomi yang terdampak pandemi untuk mengevaluasi kebijakan stimulus yang juga dicanangkan oleh pemerintah."),
                            ], className="pretty_container twelve columns",
                            style={'text-align':'center','background-color':'#fff', 'border-left':'6px solid #007bff'}
                            ),#end of column div for total SME credit channeling
                    ],className="row flex-display") #end of pred result row div
                 ],className=" twelve columns"),#end of pred result var div
    
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

        html.Div([#start of credit channeling vars
              html.H5("Penyaluran Kredit UMKM", style={"font-weight":"bold"}),
              html.Div(children=[generate_form(i) for i in np.arange(18) #row div of macro vars
                            ],className="row flex-display") #end of macro vars row div
              ],className=" twelve columns"),#end of credit channeling var div
        
        html.Div([#start of evaluation
                 html.H5("Evaluasi atas Penetapan Tarif dan Anggaran IJP Kredit UMKM", style={"font-weight":"bold"}),
                 ],className=" twelve columns"),#end of evaluation div

                        html.Div([ #start of column div for IJP tarif
                            html.H5("Tarif IJP Kredit UMKM", style={'font-weight':'bold'}),
                            html.H1(id ="IJP_tarif", style={'font-weight':'bold', 'font-size':'44px'}),
                            html.P(id="IJP_tarif_exp")
                            ], className="pretty_container three columns",
                            style={'text-align':'center','background-color':'#fff', 'border-top':'6px solid #007bff'}
                            ),#end of column div for IJP tarif
                        html.Div([ #start of column div for IJP budget
                            html.H5("Anggaran IJP", style={'font-weight':'bold'}),
                            html.H4(id ="IJP_budget", style={'font-weight':'bold', 'font-size':'32px'}),
                            html.P(id="IJP_budget_expl")
                            ], className="pretty_container four columns",
                            style={'text-align':'center','background-color':'#fff', 'border-top':'6px solid #6610f2'}
                            ),#end of column div for IJP budget
                        html.Div([ #start of column div for loss limit budget
                            html.H5("Anggaran Loss Limit", style={'font-weight':'bold'}),
                            html.H4(id ="loss_limit_budget", style={'font-weight':'bold', 'font-size':'32px'}),
                            html.P("Besaran anggaran loss limit berdasarkan penyaluran kredit yang dijaminkan")
                            ], className="pretty_container four columns",
                            style={'text-align':'center','background-color':'#fff', 'border-top':'6px solid #6f42c1'}
                            ),#end of column div for loss limit budget
        
        #affected sectors
        html.Div([ #start of total channeling and NPL row div
                        html.Div([ #start of column div for total SME Credit channeling
                            html.H5("Evaluasi atas Sektor Ekonomi Terdampak", style={"font-weight":"bold", "color":"#000"}),
                            dcc.Graph(id='channel-comparison-graph-sector-affected',
                                      style={'height':600})
                            ], className="pretty_container",
                            style={'text-align':'center','background-color':'#fff', 'border-top':'6px solid #007bff'}
                            ),#end of column div for total SME credit channeling
                        # dash_table.DataTable(
                        #     id='table-paging-and-sorting',
                        #     columns=[
                        #         {'name': 'Sektor Ekonomi', 'id': '1', 'deletable': True},
                        #         {'name': 'Proyeksi NPL', 'id': '2', 'deletable': True},
                        #         {'name': 'Proyeksi NPL Tahun 2019', 'id': '3', 'deletable': True},
                        #         {'name': 'Kenaikan (Penurunan)', 'id': '4', 'deletable': True},
                        #         ],
                        #     page_current=0,
                        #     page_size=20,
                        #     ),
                        # html.P(id="effect-analysis"),
                        # html.Div([
                        #     html.Div([
                        #         html.H5("NPL 2019", style={"font-weight":"bold", "color":"#000"}),
                        #         html.H1(id ="NPL_2019", style={'font-weight':'bold', 'font-size':'44px'}),
                        #         html.P(id="sector-name"),
                        #         ],className="four columns pretty_container", style={'text-align':'center','background-color':'#fff', 'border-top':'6px solid #007bff'}),
                        #     html.Div([
                        #         html.H5("Proyeksi NPL", style={"font-weight":"bold", "color":"#000"}),
                        #         html.H1(id ="proyeksi_NPL", style={'font-weight':'bold', 'font-size':'44px'}),
                        #         ],className="four columns pretty_container", style={'text-align':'center','background-color':'#fff', 'border-top':'6px solid #007bff'}),
                        #     html.Div([
                        #         html.H5("Naik/Turun", style={"font-weight":"bold", "color":"#000"}),
                        #         html.H1(id ="pandemic-effect", style={'font-weight':'bold', 'font-size':'44px'}),
                        #         ],className="three columns pretty_container", style={'text-align':'center','background-color':'#fff', 'border-top':'6px solid #007bff'}),
                        #     ],className="row")
                        ], className="twelve columns"), #end of total channeling and NPL row div
        
    ], className="row")])

# @app.callback(
#     Output("NPL_2019","children"),
#     Output("sector-name","children"),
#     Output("proyeksi_NPL","children"),
#     Output("pandemic-effect","children"),
#     [Input("channel-comparison-graph-sector-affected", "hoverData")])
# def hoverGraph(hoverData):
#     sector_select = hoverData['points'][0]['sector']
#     dff_2019 = df_2019[df_2019['sector']==sector_select]
    
#     return "{:,.2f} %".format(dff_2019[0]['average_NPL_2019']), sector_select,hoverData['points'][0]['percentNPL'],dff_2019[0]['average_NPL_2019']-hoverData['points'][0]['percentNPL']

@app.callback(
    [Output("sector_NPL_{}".format(i), "children") for i in np.arange(18)],
    [Output("sector_NPL_val_{}".format(i), "children") for i in np.arange(18)],
    Output("total_NPL","children"),
    Output("total_NPL_val","children"),
    Output("total_credit","children"),
    Output("IJP_tarif","children"),
    Output("IJP_budget","children"),
    Output("loss_limit_budget","children"),
    Output("IJP_tarif_exp","children"),
    Output("IJP_budget_expl","children"),
    Output("channel-comparison-graph-sector-affected","figure"),
    # Output('table-paging-and-sorting', 'data'),
    # Output("effect-analysis","children"),
    [Input("EconGrowth", "value"),
    Input("Inflasi", "value"),
    Input("Unemployment", "value"),
    Input("birate", "value"),
    Input("sector_form_0", "value"),
    Input("sector_form_1", "value"),
    Input("sector_form_2", "value"),
    Input("sector_form_3", "value"),
    Input("sector_form_4", "value"),
    Input("sector_form_5", "value"),
    Input("sector_form_6", "value"),
    Input("sector_form_7", "value"),
    Input("sector_form_8", "value"),
    Input("sector_form_9", "value"),
    Input("sector_form_10", "value"),
    Input("sector_form_11", "value"),
    Input("sector_form_12", "value"),
    Input("sector_form_13", "value"),
    Input("sector_form_14", "value"),
    Input("sector_form_15", "value"),
    Input("sector_form_16", "value"),
    Input("sector_form_17", "value"),
])
def predict_NPL(EconGrowth,Inflasi,Unemployment,birate,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r):
    
    credit_channeling = [a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r]
    
    inputPopulate = { 'SektorEkonomi': econSector,
                     'pandemicTF': [1]*18,
                     'Inflasi': [Inflasi]*18,
                      'EconGrowth':[EconGrowth]*18,
                      'Unemployment':[Unemployment]*18,
                      'valueChannel':credit_channeling,
                      'biRate':[birate]*18
        }
    
    #prediction
    percent_NPL_prediction = model_rf.predict(pd.DataFrame(inputPopulate))
    
    pre = "Proyeksi NPL Kredit UMKM untuk sektor ekonomi "
    
    #processing sectoral NPL percentage
    preds = ["{:,.2f} %".format(percent_NPL_prediction[i]*100) for i in np.arange(18)]    
    
    #processing NPL sectoral value
    pref = [pre+econSector[i]+" {:,.2f}".format(percent_NPL_prediction[i]*credit_channeling[i]) for i in np.arange(18)]
    
    #processing total NPL percentage and value
    total_SME_credit_channeling = sum(credit_channeling)
    total_NPL_val = 0.00
    for i in np.arange(18):
        NPL_i = credit_channeling[i]*percent_NPL_prediction[i]
        total_NPL_val +=NPL_i
    total_NPL_percentage = (total_NPL_val/total_SME_credit_channeling)*100
    
    s1 = pd.Series(econSector, name='sector')
    s2 = pd.Series(credit_channeling, name='channeling')
    s3 = pd.Series(percent_NPL_prediction, name='percentNPL')
    
    df = pd.concat([s1,s2,s3,average_NPL_2019], axis=1)
    df['valueNPL'] = df['percentNPL']*df['channeling']  
    df['effect'] = df['percentNPL']-df['average_NPL_2019']
    
    fig = go.Figure(go.Bar(
            x=df['percentNPL']*100,
            y=econSector,
            orientation='h'))

    #chart transition
    fig.update_layout(transition_duration=500)

    #slice df for table
    df_table = df[['sector','percentNPL','average_NPL_2019','effect']]  
        
    #top effect
    df_table_sorted = df_table.nlargest(3,'effect')
    exp_effect = "test"
    #exp_effect = "Sektor Ekonomi UMKM yang diperkirakan paling terdampak adalah sektor "+df_table_sorted[0]['sector']+", sektor "+df_table_sorted[1]['sector']+" dan sektor "+df_table_sorted[2]['sector']
    
    #processing IJP and loss limit information
    ijp_trf = ((((total_NPL_percentage/100) * 0.8)-0.01) / 0.9)*100
    ijp = ijp_trf * total_SME_credit_channeling / 100
    loss_lim = total_SME_credit_channeling / 100
    
    #data to pass
    total_NPL_percentage_pass = "{:,.2f} %".format(total_NPL_percentage)
    total_NPL_val_pass = "Proyeksi total nilai NPL atas Penyaluran Kredit kepada UMKM adalah Rp {:,.2f}".format(total_NPL_val)
    total_credit = "Rp {:,.2f}".format(total_SME_credit_channeling)
    ijp_tarif =  "{:,.2f} %".format(ijp_trf)
    ijp_tarif_expl = "Tarif IJP yang seharusnya ditetapkan berdasarkan total proyeksi NPL kredit UMKM {:,.2f} %".format(total_NPL_percentage)
    ijp_budget = "Rp {:,.2f}".format(ijp)
    ijp_budget_exp = "Besaran anggaran berdasarkan tarif IJP kredit UMKM {:,.2f} %".format(ijp_trf)
    loss_limit_budget = "Rp {:,.2f}".format(loss_lim)
    
#    return preds1, preds2, preds3, preds4, preds5, preds6, preds7, preds8, preds9, preds10, preds11, preds12, preds13, preds14, preds15, preds16, preds17, preds18, pref1, pref2, pref3, pref4, pref5, pref6, pref7, pref8, pref9, pref10, pref11, pref12, pref13, pref14, pref15, pref16, pref17, pref18, total_NPL_percentage_pass, total_NPL_val_pass, total_credit, ijp_tarif, ijp_budget, loss_limit_budget
    return preds[0], preds[1], preds[2], preds[3], preds[4], preds[5], preds[6], preds[7], preds[8], preds[9], preds[10], preds[11], preds[12], preds[13], preds[14], preds[15], preds[16], preds[17], pref[0], pref[1], pref[2], pref[3], pref[4], pref[5], pref[6], pref[7], pref[8], pref[9], pref[10], pref[11], pref[12], pref[13], pref[14], pref[15], pref[16], pref[17], total_NPL_percentage_pass, total_NPL_val_pass, total_credit, ijp_tarif, ijp_budget, loss_limit_budget, ijp_tarif_expl, ijp_budget_exp, fig