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
data['Month'] = data['Time'].dt.strftime("%B") # Extract month information
data = data.sort_values('Time')


time_frame_select = st.sidebar.selectbox(
        'Select Time Period',
        ( ['month'])
    )
    
def plotly_monthly_comparative_production(data):
    #data.drop(columns=['Unnamed: 0'], inplace=True)
    
    year_month_df= data.groupby(['Year', 'Month']).sum().reset_index()
    year_month_df.rename(columns={'Production':'Monthly_Production'}, inplace=True)
    data_year_month_df = year_month_df.merge(data, indicator=True)
    #find common columns between data and year_month_df
    #common_columns = data_year_month_df.columns.intersection(year_month_df.columns)
    #st.write(common_columns)
    data_year_month_df.sort_values('ym', inplace=True)
    data_year_month_df=data_year_month_df[['Year', 'Month', 'Monthly_Production']]
    data_year_month_df.drop_duplicates(inplace=True)
    
    
    fig = px.bar(data_year_month_df, x='Month', y='Monthly_Production', color='Year', barmode='group')

    st.plotly_chart(fig)
    
  
def main():


    st.markdown("# Comparative Production")
    st.sidebar.markdown("# Comparative Production") 
    st.subheader("Comparative Production")
    #select time period sidebar
    
   
    
    plotly_monthly_comparative_production(data)
    
if __name__ == '__main__':
    main()
