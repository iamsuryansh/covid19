import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
from matplotlib import pyplot
import datetime
import plotly.graph_objects as go
#server = app.server
DATA_URL = ("https://api.covid19india.org/csv/latest/case_time_series.csv")
DATA_URL_statewise_timeseries = ("https://api.covid19india.org/csv/latest/state_wise_daily.csv")
DATA_URL_statewise = ("https://api.covid19india.org/csv/latest/state_wise.csv")

st.title("Covid-19 in India")

statewiseData=st.sidebar.checkbox(
        "Statewise Data "
)
if statewiseData:
    st.markdown("This is a dashboard used to visualize Statewise Covid-19 situation in India ")
    series1=pd.read_csv(DATA_URL_statewise, header=0, index_col=0, parse_dates=True, squeeze=True)
    series1=series1[["Confirmed","Recovered","Deaths","Active"]]
    st.subheader("Statewise Data")
    fig = go.Figure(data=[go.Table(header=dict(values=["States","Confirmed","Recovered","Deaths","Active"]),
                 cells=dict(values=[series1.index,series1.Confirmed,series1.Recovered,series1.Deaths,series1.Active],
               fill_color='lavender',align='center'))
                     ])
    fig.update_layout(width=800, height=700)
    st.write(fig)

    selectedState = st.selectbox(
    "Select a state :",
        sorted(series1.index))
else:
    st.markdown("This is a dashboard used to visualize Covid-19 situation in India ")
    series = pd.read_csv(DATA_URL, header=0, index_col=0, parse_dates=True, squeeze=True)
    daily_confirmed = series["Daily Confirmed"]
    daily_recovered = series["Daily Recovered"]
    total_confirmed = series["Total Confirmed"]
    total_recovered = series["Total Recovered"]
    daily_deceased = series["Daily Deceased"]
    total_deceased = series["Total Deceased"]
    listOfVariables=["Daily Confirmed","Daily Recovered","Daily Deceased","Total Confirmed","Total Recovered","Total Deceased"]
    option = st.selectbox(
        'Select a category:',
        listOfVariables)
    option1=st.checkbox(
        "Select starting date")
    if option1:
        dateStart = st.sidebar.date_input('start date', datetime.date(2020,5,30))
    else:
        dateStart= datetime.date(2020,5,30)
        'Showing graph for : ', option
        option, "Cases in India since ",dateStart
        startDate1=datetime.date(2020,1,30)
        delta = dateStart-startDate1
        linedata =series[option][delta.days:]
        fig = px.line(linedata)
        fig.update_xaxes(title_text='Date')
        fig.update_layout(hovermode="x")
        fig.update_yaxes(title_text='No. of Cases')
    st.write(fig)

    total_active_today = series["Total Confirmed"][-1] - series["Total Recovered"][-1] - series["Total Deceased"][-1]
    pie = [total_active_today,series["Total Recovered"][-1],series["Total Deceased"][-1]]
    name=["Total Active Cases","Total Recovered Cases","Total Deaths"]
    colors=["lightcyan","cyan","royalblue"]
    fig1 = px.pie(pie, values=pie,names=name,
                title='Distribution of total cases in India')

    st.write(fig1)
