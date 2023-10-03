import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
from pathlib import Path
from datetime import datetime

# Load data
st.sidebar.markdown("# Production Over Time" + ':chart:')
solar_file = Path(__file__).parent.parent / "solar_production.csv"
data = pd.read_csv(solar_file, index_col=0)
data['Time'] = pd.to_datetime(data['Time'], errors='coerce')

data = data[pd.notna(data['Time'])]
start_date = data['Time'].min()
end_date = data['Time'].max()
start_date=start_date.to_pydatetime()
end_date=end_date.to_pydatetime()
# create a date slidebar to select date range
date_range = st.sidebar.slider('Select Date Range', start_date, end_date, (start_date, end_date))

#create a date slidebar to select date range




def filter_dates(date_range):
    data = data[(data['Time'] >= date_range[0]) & (data['Time'] <= date_range[1])]
    return data
#subset data to selected date range
data = data[(data['Time'] >= date_range[0]) & (data['Time'] <= date_range[1])]
data = data.sort_values('Time')


# solution plan
# i.  Convert date fields to date types using data['Time'] = pd.to_datetime(data['Time'], errors='coerce')
# ii. Drop the rows with NaT values data = data[pd.notna(data['Time'])]
# iii. Convert field to right time format for plotting
# iv. Plot Production vs Time using scatterplot

def _plot_data_over_time(data: pd.DataFrame):
    data['Time'] = pd.to_datetime(data['Time'], errors='coerce')
    data = data[pd.notna(data['Time'])]
    plt.figure(figsize=(15, 15))
    sns.scatterplot(data=data, x='Time', y='Production')
    plt.title('Production over Time', wrap=True)
    plt.xlabel('Time')
    plt.ylabel('Production')
    # increase the font of x and y ticks and labels
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    #increase the x and y labels
    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Production (kWh)', fontsize=16)
    #increase the font of the title
    plt.title('Production over Time', fontsize=20)
    return plt

def _plot_data_over_time_plotly(data: pd.DataFrame):
    # make plotly version of _plot_data_over_time function
    data['Time'] = pd.to_datetime(data['Time'], errors='coerce')
    data = data[pd.notna(data['Time'])]
    fig = px.scatter(data, x='Time', y='Production')

    #set fig size 
    fig.update_layout(height=600, width=800)
    fig.update_layout( xaxis_title='Date', yaxis_title='Production (kWh))')
    return fig

def main():


    st.markdown("# Daily Production Over Time" + ':sun_with_face:')
    
    #filtered_data=filter_dates(date_range)
    #plt=_plot_data_over_time(data)
    fig =_plot_data_over_time_plotly(data)

    #st.pyplot(plt)
    st.plotly_chart(fig)
    

    
    
if __name__ == '__main__':
    main()


