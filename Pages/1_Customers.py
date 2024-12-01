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

@st.cache_data()
def get_customer_details():
    df_cust = fetch_dataset("SELECT * FROM CUSTOMER_MASTER")
    if len(df_cust) > 0:
         df_cust.set_index('CUSTOMER ID', inplace=True)
    df_sys = fetch_dataset("SELECT * FROM GW_SYSTEM_REGISTRATION")
    return df_cust, df_sys



def get_sys_summary(df_sys):
    mthly_sys_amt = 0.0
    for i in df_sys.index:

        status = df_sys.loc[i,'SYSTEMATIC_STATUS']
        frequency = df_sys.loc[i,'FREQUENCY']
        p_day = df_sys.loc[i,'PERIOD_DAY']
        amt = float(df_sys.loc[i,'AMOUNT'].replace(",",""))

        if frequency == 'Once a Week':
            df_sys.at[i,'PERIOD_DAY'] = period_day[int(p_day)]
        elif frequency == 'Business Days(BZ)':
            df_sys.at[i,'PERIOD_DAY'] = ""

        if 'Processed' in status:
            if frequency == 'Once a Week':
                mthly_sys_amt = mthly_sys_amt + 4 * amt
            elif frequency == 'Business Days(BZ)':
                mthly_sys_amt = mthly_sys_amt + 20 * amt
            elif frequency == 'Twice a Month':
                mthly_sys_amt = mthly_sys_amt + 2 * amt
            elif frequency == 'Quarterly':
                mthly_sys_amt = mthly_sys_amt + amt/3
            elif frequency == 'Specific Date':
                mthly_sys_amt = mthly_sys_amt + len(p_day.split(",")) * amt
            elif frequency == 'Once a Month':
                mthly_sys_amt = mthly_sys_amt +  amt


    return df_sys, mthly_sys_amt




st.markdown('<p style="font-size:36px;font-weight: bold;text-align:center;vertical-align:middle;color:blue;margin:0px;padding:0px">Customer Details</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:36px;font-weight: bold;text-align:center;vertical-align:middle;color:blue;margin:0px;padding:0px"></p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:36px;font-weight: bold;text-align:center;vertical-align:middle;color:blue;margin:0px;padding:0px"></p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:36px;font-weight: bold;text-align:center;vertical-align:middle;color:blue;margin:0px;padding:0px"></p>', unsafe_allow_html=True)

df, df_sys = get_customer_details()

df_sys['FOLIO_NO']=df_sys['FOLIO_NO'].apply(lambda x: int(x.replace(",","")) if isinstance(x, str) else x)

df_sys['AMC_NAME']=df_sys['AMC_NAME'].apply(lambda x: x.split("/")[1] if isinstance(x, str) else x)
df_sys['SOURCE_SCHEME']=df_sys['SOURCE_SCHEME'].apply(lambda x: x.split("/")[1] if isinstance(x, str) else x)
df_sys['TARGET_SCHEME']=df_sys['TARGET_SCHEME'].apply(lambda x: x.split("/")[1] if pd.isnull(x) else x)

sip_cols = ['FOLIO_NO','AMC_NAME','SOURCE_SCHEME', 'FROM_DATE', 'TO_DATE', 'AMOUNT','FREQUENCY', 'PERIOD_DAY', 'SYSTEMATIC_STATUS']
stp_cols = ['FOLIO_NO', 'AMC_NAME','SOURCE_SCHEME','TARGET_SCHEME','FROM_DATE', 'TO_DATE', 'AMOUNT','FREQUENCY', 'PERIOD_DAY', 'SYSTEMATIC_STATUS']
swp_cols = ['FOLIO_NO', 'AMC_NAME','SOURCE_SCHEME','FROM_DATE', 'TO_DATE', 'AMOUNT','FREQUENCY', 'PERIOD_DAY', 'SYSTEMATIC_STATUS']



left,right = st.columns((9,3))

cust_list=[f"{i} | {df.loc[i,'INVESTOR NAME']} | {df.loc[i,'FH PAN NO']}" for i in df.index]


cust_details = left.selectbox("🔍 **Search Customer**",cust_list,3)

cust_iin_name_pan = cust_details.split("|")

if len(cust_iin_name_pan) == 3:
    cust_iin = int(cust_iin_name_pan[0].strip())
    cust_name = cust_iin_name_pan[1].strip()
    cust_pan = cust_iin_name_pan[2].strip()
st.markdown('<BR>', unsafe_allow_html=True)

df_sys_iin = df_sys[df_sys['CUSTOMER_ID'] == str(cust_iin)]

kyc, sys = st.tabs(["Personal Details", "Systematic Investments"])



with kyc:
    st.markdown('<BR>', unsafe_allow_html=True)

    c1,c2,c3,c4  = st.columns((8,7,7,7))

    tax_code = df.loc[cust_iin,'TAX STATUS CODE']
    nominee_count = df.loc[cust_iin,'NOMINEE COUNT']
    c1.markdown(display_labels("Name",cust_name), unsafe_allow_html=True)
    c2.markdown(display_labels("PAN",cust_pan), unsafe_allow_html=True)
    c3.markdown(display_labels("DOB/DOI",df.loc[cust_iin,'DOB / DOI']), unsafe_allow_html=True)
    c4.markdown(display_labels("Holding Nature",df.loc[cust_iin,'HOLDING NATURE']), unsafe_allow_html=True)

    c1.markdown(display_labels("IIN",cust_iin), unsafe_allow_html=True)
    c2.markdown(display_labels("IIN Date",df.loc[cust_iin,'CREATED DATE']), unsafe_allow_html=True)
    c3.markdown(display_labels("KYC Status",df.loc[cust_iin,'KYC STATUS']), unsafe_allow_html=True)
    c4.markdown(display_labels("Tax Status",tax_code), unsafe_allow_html=True)

    c1.markdown(display_labels("Email",df.loc[cust_iin,'EMAIL']), unsafe_allow_html=True)
    c2.markdown(display_labels("Email Relationship",df.loc[cust_iin,'EMAIL RELATION']), unsafe_allow_html=True)
    c3.markdown(display_labels("Mobile No",df.loc[cust_iin,'MOBILE NO']), unsafe_allow_html=True)
    c4.markdown(display_labels("Mobile Relationship",df.loc[cust_iin,'MOBILE RELATION']), unsafe_allow_html=True)

    if 'NRI' in tax_code.upper():
        address = f"{df.loc[cust_iin,'NRI ADDRESS1']}, {df.loc[cust_iin,'NRI ADDRESS2']}, {df.loc[cust_iin,'NRI CITY']}, {df.loc[cust_iin,'NRI STATE']}, {df.loc[cust_iin,'NRI COUNTRY']}, {int(df.loc[cust_iin,'NRI PINCODE'])}"
        st.markdown(display_labels("Address",address.replace('nan,','').replace(",,",",")), unsafe_allow_html=True)
    else:
        address = f"{df.loc[cust_iin,'ADDRESS1']}, {df.loc[cust_iin,'ADDRESS2']}, {df.loc[cust_iin,'CITY']}, {df.loc[cust_iin,'STATE']}, {df.loc[cust_iin,'COUNTRY']}, {int(df.loc[cust_iin,'PINCODE'])}"
        st.markdown(display_labels("Address",address.replace('nan,','').replace(",,",",")), unsafe_allow_html=True)

    nominee = f"{df.loc[cust_iin,'NOM1 NAME']}, {df.loc[cust_iin,'NOM1 RELATION']}, {df.loc[cust_iin,'NOM1 PERCENTAGE']}"
    nom2 = df.loc[cust_iin,'NOM2 NAME']

    if nom2 is not None :
        nominee = f"{nominee} | {df.loc[cust_iin,'NOM2 NAME']}, {df.loc[cust_iin,'NOM2 RELATION']}, {df.loc[cust_iin,'NOM2 PERCENTAGE']}"
        nom3 = df.loc[cust_iin,'NOM3 NAME']

        if nom3 is not None:
            nominee = f"{nominee} | {df.loc[cust_iin,'NOM3 NAME']}, {df.loc[cust_iin,'NOM3 RELATION']}, {df.loc[cust_iin,'NOM3 PERCENTAGE']}"

    st.markdown(display_labels("Nominees",nominee), unsafe_allow_html=True)

with sys:


    c1,c2,c3  = st.columns((8,6,7))

    c1.markdown(display_labels("IIN",int(cust_iin)), unsafe_allow_html=True)
    c2.markdown(display_labels("Name",cust_name), unsafe_allow_html=True)
    placeholder = c3.empty()

    if len(df_sys_iin) > 0:
        radio_opts = [i for i in df_sys_iin['AUTO_TRXN_TYPE'].unique()]

        selected_option = st.radio("Choose Systematic Investment Type:", radio_opts, index=0)

        df_sys_iin_sip = df_sys_iin[df_sys_iin['AUTO_TRXN_TYPE']=='SIP'][sip_cols].sort_values(by='SYSTEMATIC_STATUS',ascending=False)
        df_sys_iin_stp = df_sys_iin[df_sys_iin['AUTO_TRXN_TYPE']=='STP'][stp_cols].sort_values(by='SYSTEMATIC_STATUS',ascending=False)
        df_sys_iin_swp = df_sys_iin[df_sys_iin['AUTO_TRXN_TYPE']=='SWP'][swp_cols].sort_values(by='SYSTEMATIC_STATUS',ascending=False)

        if selected_option == 'SIP':
            sys_summary, mthly_sys = get_sys_summary(df_sys_iin_sip)
            placeholder.markdown(display_labels("Monthly SIP Amount",display_amount(mthly_sys)), unsafe_allow_html=True)
            st.markdown(get_markdown_table(sys_summary, footer='N'),unsafe_allow_html=True)
            st.markdown('<BR>', unsafe_allow_html=True)
        elif selected_option == 'STP':
            sys_summary, mthly_sys = get_sys_summary(df_sys_iin_stp)
            placeholder.markdown(display_labels("Monthly STP Amount",display_amount(mthly_sys)), unsafe_allow_html=True)
            st.markdown(get_markdown_table(sys_summary, footer='N'),unsafe_allow_html=True)
            st.markdown('<BR>', unsafe_allow_html=True)

        elif selected_option == 'SWP':
            sys_summary, mthly_sys = get_sys_summary(df_sys_iin_swp)
            placeholder.markdown(display_labels("Monthly SWP Amount",display_amount(mthly_sys)), unsafe_allow_html=True)
            st.markdown(get_markdown_table(sys_summary, footer='N'),unsafe_allow_html=True)
            st.markdown('<BR>', unsafe_allow_html=True)

    else:
        st.markdown(
            """
            <p style="color:blue; font-weight:bold;">
                No Systematic Investment Registered
            </p>
            """,
            unsafe_allow_html=True
        )
