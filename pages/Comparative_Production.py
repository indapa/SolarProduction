import streamlit as st
import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys
import plotly.express as px
import numpy as np
from st_aggrid import AgGrid
import plotly.graph_objects as go


# Load data
solar_file = Path(__file__).parent.parent / "solar_production.csv"


st.sidebar.markdown("# Comparative Production" + ':chart:') 
time_frame_select = st.sidebar.selectbox(
        'Select Time Period',
        ( ['year', 'month', 'quarter', 'cumulative'])
    )
# plot cumulative production by year, with each year as  line
def plotly_yearly_production():
    q = (
        pl.scan_csv("MonthlyData/*.csv")
         .select(
            # Convert the Time column to a proper date
            pl.col("Time")
            .str.strptime(pl.Date, format="%m/%d/%Y")
            .alias("Date"),
            # Divide by 1000 and alias as kWh for clarity
             (pl.col("System Production (Wh)") / 1000)
             .alias("Production"),
            
    
        )
        .with_columns (
            year_str = pl.col("Date").dt.strftime("%Y"),
            year_num = pl.col("Date").dt.year(),
            month_str = pl.col("Date").dt.strftime("%B"),
            month_num = pl.col("Date").dt.month(),
        )
        .group_by([pl.col("year_num"), pl.col("year_str")])
        # Now compute the year sum
        .agg(
            pl.col("Production").sum().round(2).alias("Yearly_Production")
        )
        # round avg_production_kWh to 2 decimal places
    
        .sort(["year_num"])
        
    )
    
    year_df = q.collect()
    
    
    
    fig = px.bar(year_df, x='year_str', y='Yearly_Production', color='year_str', barmode='group')
    
    # adjust offset and  width so bars are centered nicely
    fig.update_traces(offset= -.2, width=0.4)
    
    # Improve layout
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Yearly Production (kWh)",
        xaxis=dict(type='category'),  # ensure x-axis is treated as categorical
        bargap=0.2                    # play with bargap for spacing
    )
    
    fig.update_layout(xaxis_title="Year", yaxis_title="Yearly Production (kWh)")
    st.plotly_chart(fig)


def plotly_monthly_production_new(data):
    
    combined_df = pd.read_csv(solar_file, index_col=0)
    combined_df['Time'] = pd.to_datetime(data['Time'])  # Convert to datetime format
    
    combined_df['MMDD'] = combined_df['Time'].dt.strftime('%m-%d')
    combined_df['MMDD'] = pd.to_datetime(combined_df['MMDD'], format='%m-%d', errors='coerce')
    combined_df['MMDD'] = combined_df['MMDD'].apply(lambda x: x.replace(year=2024))


    combined_df['YYYY'] = combined_df['Time'].dt.strftime('%Y')

#add a column for cumulative production by year

    combined_df['Cumulative Production'] = combined_df.groupby('YYYY')['Production'].cumsum()
    combined_df.sort_values(by=['YYYY', 'MMDD'], inplace=True)
    fig = px.line(combined_df, x='MMDD', y='Cumulative Production', color='YYYY',
              title='Cumulative Solar Production by Year',
              labels={'YYYY': 'Year', 'MMDD': 'Month', 'Cumulative Production': 'Cumulative Production'})
    fig.update_xaxes(dtick="M1", tickformat="%b")
    
    st.plotly_chart(fig,use_container_width=True)
# plot cumulative production by year
def plotly_cumulative_production(data):
    
    data['Cumulative Production'] = data.groupby('Year')['Production'].cumsum()
    fig = go.Figure()
    
    for year, data in data.groupby('Year'):
        fig.add_trace(go.Scatter(x=data['Time'], y=data['Cumulative Production'], mode='lines', name=f'Year {year}'))

    fig.update_layout(title='Cumulative Production Over Time', xaxis_title='Date', yaxis_title='Cumulative Production')
    
    
    st.plotly_chart(fig,use_container_width=True)

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
    year_df['Year'] = year_df['Year'].astype('category')
    fig = px.bar(year_df, x='Year', y='Yearly_Production', color='Year', barmode='group')
    
    # adjust offset and  width so bars are centered nicely
    fig.update_traces(offset= -.2, width=0.4)
    
    # Improve layout
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Yearly Production (kWh)",
        xaxis=dict(type='category'),  # ensure x-axis is treated as categorical
        bargap=0.2                    # play with bargap for spacing
    )
    
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
        plotly_yearly_production()
    elif time_frame_select == 'month':  
        plotly_monthly_comparative_production(data)
    elif time_frame_select == 'cumulative':
        #plotly_cumulative_production(data)
        plotly_monthly_production_new(data)
    else:
        plotly_quarterly_comparative_production(data)

    
    
if __name__ == '__main__':
    main()
