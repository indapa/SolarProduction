import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys
import plotly.express as px
import numpy as np
from st_aggrid import AgGrid

# Load data
solar_file = Path(__file__).parent.parent / "solar_production.csv"

data = pd.read_csv(solar_file, index_col=0)
data['Time'] = pd.to_datetime(data['Time'])  # Convert to datetime format
data['ym']=data['Time'].dt.strftime('%Y-%m')
data['Year'] = data['Time'].dt.strftime("%Y") # Extract year information
data['Month'] = data['Time'].dt.strftime("%m") # Extract month information
data['Month'] = pd.to_numeric(data['Month'])
data['Year'] = pd.to_numeric(data['Year'])
data = data.sort_values('Time')

st.sidebar.markdown("# Comparative Production" + ':chart:') 
time_frame_select = st.sidebar.selectbox(
        'Select Time Period',
        ( ['month', 'year', 'quarter'])
    )

# plot quarterly comparative production
def plotly_quarterly_comparative_production(data):
    
    conditions = [ (data['Month'] <=3), (data['Month']  <=6), (data['Month'] <=9), (data['Month'] <=12)]
    values = ['Q1', 'Q2', 'Q3', 'Q4']
    data['Quarter']= np.select(conditions, values)
    
    data=data[['Year', 'Quarter', 'Production']]
    year_quarter_df= data.groupby(['Year', 'Quarter']).sum().reset_index()
    year_quarter_df.rename(columns={'Production':'Quarterly_Production'}, inplace=True)
    year_quarter_df['Year'] = year_quarter_df['Year'].astype(str)
    fig = px.bar(year_quarter_df, x='Quarter', y='Quarterly_Production', color='Year', barmode='group')
    fig.update_layout(xaxis_title="Quarter", yaxis_title="Quarterly Production (kWh)")
    st.plotly_chart(fig)

# plot yearly compparative production
def plotly_yearly_comparative_production(data):
    data=data[['Year', 'Production']]
    year_df= data.groupby(['Year']).sum().reset_index()
    year_df.rename(columns={'Production':'Yearly_Production'}, inplace=True)
    year_df['Year'] = year_df['Year'].astype(str)
    fig = px.bar(year_df, x='Year', y='Yearly_Production', color='Year', barmode='group')
    
    fig.update_layout(xaxis_title="Year", yaxis_title="Yearly Production (kWh)")
    st.plotly_chart(fig)

def plotly_monthly_comparative_production(data):
    data=data[['Year', 'Month', 'Production']]
    
    year_month_df= data.groupby(['Year', 'Month']).sum().reset_index()
    year_month_df.rename(columns={'Production':'Monthly_Production'}, inplace=True)
    year_month_df['Month'] = pd.to_numeric(year_month_df['Month'])
    year_month_df['Year'] = pd.to_numeric(year_month_df['Year'])

    numeric_to_abbr={ 1:'January',
                    2:'February',
                    3:'March',
                    4:'April',
                    5:'May',
                    6:'June',
                    7:'July',
                    8:'August',
                    9:'September',
                    10:'October',
                    11:'November',
                    12:'December'}
    year_month_df=year_month_df.replace({"Month": numeric_to_abbr})
    year_month_df['Year'] = year_month_df['Year'].astype(str)

    
    fig = px.bar(year_month_df, x='Month', y='Monthly_Production', color='Year', barmode='group')
    fig.update_layout(xaxis_title="Month", yaxis_title="Monthly Production (kWh)")

    st.plotly_chart(fig)
    
  
def main():


    st.markdown("# Comparative Production" + ':sun_with_face:')
    
    
    #select time period sidebar
    
    
    if time_frame_select == 'year':
        plotly_yearly_comparative_production(data)
    elif time_frame_select == 'month':  
        plotly_monthly_comparative_production(data)
    else:
        plotly_quarterly_comparative_production(data)

    
    
if __name__ == '__main__':
    main()
