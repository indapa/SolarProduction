import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys
import plotly.express as px


st.sidebar.markdown("# Daily production" +  ':chart:')
solar_file = Path(__file__).parent / "solar_production.csv"
# Load data
data = pd.read_csv(solar_file)

#d
data['Time'] = pd.to_datetime(data['Time'])  # Convert to datetime format
data['Year'] = data['Time'].dt.strftime("%Y") # Extract year information
data['Month'] = data['Time'].dt.strftime("%B") # Extract month information
years = data['Year'].unique()
# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'Select Year',
    ( years ), index=2
)

#subset data to selected year
data = data[data['Year'] == add_selectbox]



data['cumulative']=data['Production'].cumsum()
# Streamlit app code
def main():
    

    # Display the loaded data
    
   

    # Plotting the data
    st.markdown("# Daily Production" + ':sun_with_face:')
    
    st.write('You selected:', add_selectbox)
    #plot_power_production(data)
    plot_power_production_plotly(data)


    # Plotting cumulative power production
    st.markdown("# Cumulative Solar Production"  + ':sun_with_face:')
    #plot_cumulative_power_production(data)
    plot_cumulative_power_production_plotly(data)

# function to plot power function in plotly
def plot_power_production_plotly(data):
    #data['Time'] = pd.to_datetime(data['Time'])  # Convert to datetime format
    #data['Month'] = data['Time'].dt.strftime("%B") # Extract month information
    
    fig = px.box(data, x='Month', y='Production', color='Month', points="all", 
                 width=900, height=900)
       
    fig.update_traces(quartilemethod="exclusive")  # or "inclusive", or "linear" by default
    fig.update_layout(xaxis_title="Month", yaxis_title="Production (kWh)")
    st.plotly_chart(fig)


    



def plot_cumulative_power_production_plotly(data):
    fig = px.line(data, x='Time', y='cumulative', width=900, height=900)
    fig.update_layout(xaxis_title="Time", yaxis_title="Cumulative Production (kWh)")
    st.plotly_chart(fig)
  

if __name__ == '__main__':
    main()
