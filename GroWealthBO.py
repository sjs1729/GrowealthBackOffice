import streamlit as st
import numpy as np
import pandas as pd
import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from scipy import optimize
import math
import time
from urllib.request import urlopen
import json
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

months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

c_1, c_2 = st.columns((8,4))
c_2.image('growealth-logo_long.png', width=300)

st.markdown('<p style="font-size:36px;font-weight: bold;text-align:center;vertical-align:middle;color:blue;margin:0px;padding:0px">Growealth Operations</p>', unsafe_allow_html=True)


st.cache_data()
def get_gw_comm_aum_data():
    df_comm = pd.read_csv("GW_Commission.csv")
    df_aum = pd.read_csv("GW_AUM.csv")


    #df_comm['TOTAL'] = df_comm.sum(axis=1)
    #df_aum['TOTAL'] = df_aum.sum(axis=1)


    return df_comm, df_aum

@st.cache_data()
def fetch_aum(query):
    return fetch_dataset(query)

st.cache_data()
def fetch_commission(query):
    return fetch_dataset(query)

df_aum = fetch_aum("SELECT * FROM GW_AUM")
df_comm = fetch_commission("SELECT * FROM GW_COMMISSION")
df_aum['Period'] = pd.to_datetime(df_aum['Period'])
df_aum['Period'] = df_aum['Period'].apply(lambda x: x.date())
df_comm['Period'] = df_aum['Period'].apply(lambda x: x)

df_aum.set_index('Period', inplace=True)
df_comm.set_index('Period', inplace=True)





df_comm['TOTAL'] = df_comm.sum(axis=1)
df_aum['TOTAL'] = df_aum.sum(axis=1)


curr_mth = f"{months[df_comm.index[-1].month -1]}-{df_comm.index[-1].year}"
curr_aum = df_aum['TOTAL'].iloc[-1]
curr_commission = df_comm['TOTAL'].iloc[-1]

df_comm = round(df_comm /1000.0,2)
df_aum = round(df_aum /10000000.0,2)

dict_aum_comm =  {
    "AUM": curr_aum,
    "Commission": curr_commission
}
min_range = df_comm['TOTAL'].min()
max_range = 2 * df_comm['TOTAL'].max()

st.markdown('<BR><BR>', unsafe_allow_html=True)

col1,col2,col3 = st.columns((6,5,6))
col1.markdown('<BR>', unsafe_allow_html=True)
col1.markdown(f'<p style="font-size:18px;font-weight: bold;text-align:left;vertical-align:middle;color:darkgreen;margin:0px;padding:0px">Current Month Snapshot - {curr_mth}</p>', unsafe_allow_html=True)
col1.markdown('<BR>', unsafe_allow_html=True)
col1.markdown(get_markdown_dict(dict_aum_comm, font_size = 15, format_amt = 'A'), unsafe_allow_html=True)
st.markdown('<BR><BR>', unsafe_allow_html=True)

report_columns = ['Axis', 'Canara Robeco', 'HDFC', 'ICICI Prudential', 'Kotak',
       'Mirae', 'Nippon India', 'PGIM India', 'SBI', 'Quant', 'Motilal Oswal',
       'HSBC', 'UTI','PARAG PARIKH']


date_options = [i for i in df_comm.index[11:]]

slider_date = st.select_slider("Select 12 Months End Date",
        options=date_options,
        value=date_options[-1]  # Default to the full range
    )

st.markdown('<BR><BR>', unsafe_allow_html=True)

#st.write(slider_date)
df_aum_1 = df_aum[df_aum.index <= slider_date].tail(12)
df_comm_1 = df_comm[df_comm.index <= slider_date].tail(12)

config = {'displayModeBar': False}

# Create a Plotly figure
# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])





# Add a bar chart for profit from df2
fig.add_trace(go.Bar(
    x=df_comm_1.index,
    y=df_comm_1['TOTAL'],
    name='Commission',
    marker=dict(color='green'))
    , secondary_y=True
)

# Add a line chart for sales from df1
fig.add_trace(go.Scatter(
    x=df_aum_1.index,
    y=df_aum_1['TOTAL'],
    mode='lines+markers',
    name='AUM',
    line=dict(color='blue', width=3),
    marker=dict(color='red',
        size=8  # Set the marker size here
    )
))

# Update layout
fig.update_layout(
    title=f"AUM Growth & Commission (Last 12 Mths ending {slider_date.strftime('%b %y')})",
    title_x=0.3,
    title_y=1,
    title_font_size=16,
    xaxis_title="Period",
    yaxis_title="AUM (in Cr)",
    yaxis2=dict(
        title="Commission (in '000)",  # Custom label for secondary y-axis
        overlaying='y',           # Secondary axis shares the same x-axis
        side='right',             # Place secondary axis on the right
        range = [0, max_range],
        showgrid=False
    ),
    barmode='group',  # Group bars and line chart on the same x-axis
    legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="left", x=0.02),
)

fig.update_layout(height=500)
fig.update_layout(width=550)


# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)



st.write("----------------")

df_comm_2 = df_comm[df_comm.index == slider_date][report_columns].transpose()

#st.write(df_comm_2)


fig1 = px.bar(df_comm_2)
fig1.update_layout(title_text=f"Commission by AMC for {slider_date.strftime('%b %y')}",
                  title_x=0.4,
                  title_y=1,
                  title_font_size=16,
                  xaxis_title="Fund Houses",
                  yaxis_title="Monthly Commission ('000')")

fig1.update_layout(margin=dict(l=1,r=1,b=1,t=18))
fig1.update_xaxes(showgrid=True)
fig1.update_layout(legend_title='')
fig1.update_layout(showlegend=False)
fig1.update_layout(height=350)
fig1.update_layout(width=550)
fig1.update_layout(legend=dict(
        yanchor="bottom",
        y=0.9,
        xanchor="left",
        x=0.05
    ))

st.plotly_chart(fig1, use_container_width=True)
