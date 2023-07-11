import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys
import plotly.express as px

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
        ( ['month'])
    )
    
def plotly_monthly_comparative_production(data):
    
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

    st.plotly_chart(fig)
    
  
def main():


    st.markdown("# Comparative Production")
    
    st.subheader("Comparative Production")
    #select time period sidebar
    
    
    
    plotly_monthly_comparative_production(data)
    
if __name__ == '__main__':
    main()
