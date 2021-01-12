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

                        html.Div([ #start of total channeling and NPL row div
                        html.Div([ #start of column div for total SME Credit channeling
                            html.H5("Total Penyaluran Kredit UMKM", style={'font-weight':'bold'}),
                            html.H4(id ="total_credit", style={'font-weight':'bold', 'font-size':'36px'}),
                            ], className="pretty_container six columns",
                            style={'text-align':'center','background-color':'#fff', 'border-top':'6px solid #fd7e14'}
                            ),#end of column div for total SME credit channeling
                        html.Div([ #start of column div for total NPL Projection
                            html.H5("Proyeksi Total NPL Kredit UMKM", style={'font-weight':'bold'}),
                            html.H1(id ="total_NPL", style={'font-weight':'bold', 'font-size':'44px'}),
                            html.P(id="total_NPL_val")
                            ], className="pretty_container six columns",
                            style={'text-align':'center','background-color':'#fff', 'border-top':'6px solid #ffc107'}
                            )#end of column div for total NPL projection
                        ], className="row flex-display"), #end of total channeling and NPL row div
                    
                    html.Div([ #start of budgeting row div
                        html.Div([ #start of column div for IJP tarif
                            html.H5("Tarif IJP Kredit UMKM", style={'font-weight':'bold'}),
                            html.H1(id ="IJP_tarif", style={'font-weight':'bold', 'font-size':'44px'}),
                            html.P(id="IJP_tarif_exp")
                            ], className="pretty_container four columns",
                            style={'text-align':'center','background-color':'#fff', 'border-top':'6px solid #007bff'}
                            ),#end of column div for IJP tarif
                        html.Div([ #start of column div for IJP budget
                            html.H5("Anggaran IJP", style={'font-weight':'bold'}),
                            html.H4(id ="IJP_budget", style={'font-weight':'bold', 'font-size':'32px'}),
                            ], className="pretty_container four columns",
                            style={'text-align':'center','background-color':'#fff', 'border-top':'6px solid #6610f2'}
                            ),#end of column div for IJP budget
                        html.Div([ #start of column div for loss limit budget
                            html.H5("Anggaran Loss Limit", style={'font-weight':'bold'}),
                            html.H4(id ="loss_limit_budget", style={'font-weight':'bold', 'font-size':'32px'}),
                            ], className="pretty_container four columns",
                            style={'text-align':'center','background-color':'#fff', 'border-top':'6px solid #6f42c1'}
                            ),#end of column div for loss limit budget
                        ], className="row flex-display"), #end of budgeting row div
    
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
    ], className="row pretty_container")])

@app.callback(
    [Output("sector_NPL_{}".format(i), "children") for i in np.arange(18)],
    [Output("sector_NPL_val_{}".format(i), "children") for i in np.arange(18)],
    Output("total_NPL","children"),
    Output("total_NPL_val","children"),
    Output("total_credit","children"),
    Output("IJP_tarif","children"),
    Output("IJP_budget","children"),
    Output("loss_limit_budget","children"),
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
    Input("sector_form_17", "value")
])
def predict_NPL(EconGrowth,Inflasi,Unemployment,birate,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r):
    
    #prediction
    pred1 = model_rf.predict([[econSector[0], 1, Inflasi, EconGrowth, Unemployment, a/1000000000, birate]])
    pred2 = model_rf.predict([[econSector[1], 1, Inflasi, EconGrowth, Unemployment, b/1000000000, birate]])    
    pred3 = model_rf.predict([[econSector[2], 1, Inflasi, EconGrowth, Unemployment, c/1000000000, birate]])
    pred4 = model_rf.predict([[econSector[3], 1, Inflasi, EconGrowth, Unemployment, d/1000000000, birate]])
    pred5 = model_rf.predict([[econSector[4], 1, Inflasi, EconGrowth, Unemployment, e/1000000000, birate]])
    pred6 = model_rf.predict([[econSector[5], 1, Inflasi, EconGrowth, Unemployment, f/1000000000, birate]])
    pred7 = model_rf.predict([[econSector[6], 1, Inflasi, EconGrowth, Unemployment, g/1000000000, birate]])
    pred8 = model_rf.predict([[econSector[7], 1, Inflasi, EconGrowth, Unemployment, h/1000000000, birate]])
    pred9 = model_rf.predict([[econSector[8], 1, Inflasi, EconGrowth, Unemployment, i/1000000000, birate]])
    pred10 = model_rf.predict([[econSector[9], 1, Inflasi, EconGrowth, Unemployment, j/1000000000, birate]])
    pred11 = model_rf.predict([[econSector[10], 1, Inflasi, EconGrowth, Unemployment, k/1000000000, birate]])
    pred12 = model_rf.predict([[econSector[11], 1, Inflasi, EconGrowth, Unemployment, l/1000000000, birate]])
    pred13 = model_rf.predict([[econSector[12], 1, Inflasi, EconGrowth, Unemployment, m/1000000000, birate]])
    pred14 = model_rf.predict([[econSector[13], 1, Inflasi, EconGrowth, Unemployment, n/1000000000, birate]])
    pred15 = model_rf.predict([[econSector[14], 1, Inflasi, EconGrowth, Unemployment, o/1000000000, birate]])
    pred16 = model_rf.predict([[econSector[15], 1, Inflasi, EconGrowth, Unemployment, p/1000000000, birate]])
    pred17 = model_rf.predict([[econSector[16], 1, Inflasi, EconGrowth, Unemployment, q/1000000000, birate]])
    pred18 = model_rf.predict([[econSector[17], 1, Inflasi, EconGrowth, Unemployment, r/1000000000, birate]])    
    
    pre = "Proyeksi NPL Kredit UMKM untuk sektor ekonomi "
    
    #processing sectoral NPL percentage
    preds1 = "{:,.2f} %".format(pred1[0]*100)
    preds2 = "{:,.2f} %".format(pred2[0]*100)
    preds3 = "{:,.2f} %".format(pred3[0]*100)
    preds4 = "{:,.2f} %".format(pred4[0]*100)
    preds5 = "{:,.2f} %".format(pred5[0]*100)
    preds6 = "{:,.2f} %".format(pred6[0]*100)
    preds7 = "{:,.2f} %".format(pred7[0]*100)
    preds8 = "{:,.2f} %".format(pred8[0]*100)
    preds9 = "{:,.2f} %".format(pred9[0]*100)
    preds10 = "{:,.2f} %".format(pred10[0]*100)
    preds11 = "{:,.2f} %".format(pred11[0]*100)
    preds12 = "{:,.2f} %".format(pred12[0]*100)
    preds13 = "{:,.2f} %".format(pred13[0]*100)
    preds14 = "{:,.2f} %".format(pred14[0]*100)
    preds15 = "{:,.2f} %".format(pred15[0]*100)
    preds16 = "{:,.2f} %".format(pred16[0]*100)
    preds17 = "{:,.2f} %".format(pred17[0]*100)
    preds18 = "{:,.2f} %".format(pred18[0]*100)
    
    #processing NPL sectoral value
    pref1 = pre+econSector[0]+" {:,.2f}".format(pred1[0]*a)
    pref2 = pre+econSector[1]+" {:,.2f}".format(pred2[0]*b)
    pref3 = pre+econSector[2]+" {:,.2f}".format(pred3[0]*c)
    pref4 = pre+econSector[3]+" {:,.2f}".format(pred4[0]*d)
    pref5 = pre+econSector[4]+" {:,.2f}".format(pred5[0]*e)
    pref6 = pre+econSector[5]+" {:,.2f}".format(pred6[0]*f)
    pref7 = pre+econSector[6]+" {:,.2f}".format(pred7[0]*g)
    pref8 = pre+econSector[7]+" {:,.2f}".format(pred8[0]*h)
    pref9 = pre+econSector[8]+" {:,.2f}".format(pred9[0]*i)
    pref10 = pre+econSector[9]+" {:,.2f}".format(pred10[0]*j)
    pref11 = pre+econSector[10]+" {:,.2f}".format(pred11[0]*k)
    pref12 = pre+econSector[11]+" {:,.2f}".format(pred12[0]*l)
    pref13 = pre+econSector[12]+" {:,.2f}".format(pred13[0]*m)
    pref14 = pre+econSector[13]+" {:,.2f}".format(pred14[0]*n)
    pref15 = pre+econSector[14]+" {:,.2f}".format(pred15[0]*o)
    pref16 = pre+econSector[15]+" {:,.2f}".format(pred16[0]*p)
    pref17 = pre+econSector[16]+" {:,.2f}".format(pred17[0]*q)
    pref18 = pre+econSector[17]+" {:,.2f}".format(pred18[0]*r)
    
    #populate variables
    credit_channeling = [a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r]
    percent_NPL_prediction = [pred1[0],pred2[0],pred3[0],pred4[0],pred5[0],pred6[0],
                           pred7[0],pred8[0],pred9[0],pred10[0],pred11[0],pred12[0],
                           pred13[0],pred14[0],pred15[0],pred16[0],pred17[0],pred18[0]]
    
    #processing total NPL percentage and value
    total_SME_credit_channeling = sum(credit_channeling)
#    populate_total_NPL = [[credit_channeling[_]*percent_NPL_prediction[_]/100] for _ in np.arange(18)]
    total_NPL_val = 0.00
    for i in np.arange(18):
        NPL_i = credit_channeling[i]*percent_NPL_prediction[i]
        total_NPL_val +=NPL_i
    total_NPL_percentage = (total_NPL_val/total_SME_credit_channeling)*100
    
    #processing IJP and loss limit information
    #ijp_trf = total_NPL_percentage * 0.8 * 0.91
    ijp_trf = ((((total_NPL_percentage/100) * 0.8)-0.01) / 0.9)*100
    ijp = ijp_trf * total_SME_credit_channeling / 100
    #loss_lim = ijp / 100
    loss_lim = total_SME_credit_channeling / 100
    
    #data to pass
    total_NPL_percentage_pass = "{:,.2f} %".format(total_NPL_percentage)
    total_NPL_val_pass = "Proyeksi total nilai NPL atas Penyaluran Kredit kepada UMKM adalah Rp {:,.2f}".format(total_NPL_val)
    total_credit = "Rp {:,.2f}".format(total_SME_credit_channeling)
    ijp_tarif =  "{:,.2f} %".format(ijp_trf)
    ijp_budget = "Rp {:,.2f}".format(ijp)
    loss_limit_budget = "Rp {:,.2f}".format(loss_lim)
    
    return preds1, preds2, preds3, preds4, preds5, preds6, preds7, preds8, preds9, preds10, preds11, preds12, preds13, preds14, preds15, preds16, preds17, preds18, pref1, pref2, pref3, pref4, pref5, pref6, pref7, pref8, pref9, pref10, pref11, pref12, pref13, pref14, pref15, pref16, pref17, pref18, total_NPL_percentage_pass, total_NPL_val_pass, total_credit, ijp_tarif, ijp_budget, loss_limit_budget