import streamlit as st
import numpy as np
import pandas as pd
import datetime as dt
import plotly.graph_objects as go
#from plotly.subplots import make_subplots
import plotly.express as px
from scipy.optimize import minimize
from scipy import optimize
import random
import math
from shared_functions import *
from db_functions import *

from shared_functions import *

st.set_page_config(
    page_title="GroWealth Investments       ",
    page_icon="nirvana.ico",
    layout="wide",
)


np.set_printoptions(precision=3)

tday = dt.datetime.today()

st.markdown(
    """
    <style>
    .css-k1vhr4 {
        margin-top: -60px;
    }


    </style>
    """,
    unsafe_allow_html=True
)
c_1, c_2 = st.columns((8,4))
c_2.image('growealth-logo_long.png')



period_day = ['SAT','SUN','MON','TUE','WED','THU','FRI']
scheme_cols=['Scheme_Name','Fund_House','Asset_Type','Scheme_Category','Scheme_Start_Date','NAV','NAV_Date','GW_Brokerage']




st.markdown('<p style="font-size:36px;font-weight: bold;text-align:center;vertical-align:middle;color:blue;margin:0px;padding:0px">MF Schemes</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:36px;font-weight: bold;text-align:center;vertical-align:middle;color:blue;margin:0px;padding:0px"></p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:36px;font-weight: bold;text-align:center;vertical-align:middle;color:blue;margin:0px;padding:0px"></p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:36px;font-weight: bold;text-align:center;vertical-align:middle;color:blue;margin:0px;padding:0px"></p>', unsafe_allow_html=True)

df = fetch_all_schemes()
if df is not None:
    df.set_index('Amfi_Code', inplace=True)

fund_perf,fund_brkg = st.tabs([ "Fund Performance", "Set Fund Brokerage"])


with fund_brkg:


    c1,c2  = st.columns((7,5))
    asset_list = [i for i in df['Asset_Type'].unique()]
    asset_list.insert(0,'ALL')
    asset_type = c1.selectbox("Fund Type",asset_list,0)

    if asset_type == 'ALL':
        df_at = df
    else:
        df_at = df[df['Asset_Type'] == asset_type ]

    cat_list = [i for i in df_at['Scheme_Category'].unique()]
    cat_list.insert(0,'ALL')

    scheme_cat = c2.selectbox('Scheme Category',cat_list,0)

    if scheme_cat == 'ALL':
        df_at_cat = df_at
    else:
        df_at_cat = df_at[df_at['Scheme_Category'] == scheme_cat ]

    scheme_list = [f"{i}|{df_at_cat.loc[i,'Scheme_Name']}|{df_at_cat.loc[i,'GW_Brokerage']}" for i in df_at_cat.index]

    scheme = st.selectbox("🔍 **Search Scheme**",scheme_list,0)


    c1,c2,c3,c4  = st.columns((6,12,3,6))

    schm_details = scheme.split("|")

    sch_code = schm_details[0]
    #st.write(schm_details[2])

    c1.markdown(display_labels("Amfi Code",sch_code), unsafe_allow_html=True)
    c2.markdown(display_labels("Name",schm_details[1]), unsafe_allow_html=True)
    c3.markdown(display_labels("Brokerage",""), unsafe_allow_html=True)
    new_brokerage = c4.number_input("Set Brokerage",min_value=0.0,max_value=2.0,step=0.01,value=float(schm_details[2]),label_visibility="collapsed", key="brokerage")
    #st.write(st.session_state)

    n_ok = c4.button("Update Brokerage")

    if n_ok:
        rows_updated = update_brokerage(int(sch_code), new_brokerage)

        if rows_updated >0 :
            st.success(f"{rows_updated} rows updated successfully")
            #fetch_all_schemes.clear()
        else:
            st.error(f"Data not saved")


with fund_perf:
    st.dataframe(df)
