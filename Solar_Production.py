import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys
import plotly.express as px
from st_aggrid import AgGrid
st.set_page_config(layout="wide")
st.sidebar.markdown("# Daily production" +  ':chart:')
solar_file = Path(__file__).parent / "solar_production.csv"
# Load data
data = pd.read_csv(solar_file, index_col=0)


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


# function to plot power function in plotly
def plot_power_production_plotly(data):
    #data['Time'] = pd.to_datetime(data['Time'])  # Convert to datetime format
    #data['Month'] = data['Time'].dt.strftime("%B") # Extract month information
    
    fig = px.box(data, x='Month', y='Production', color='Month', points="all", 
                 width=900, height=900)
       
    fig.update_traces(quartilemethod="exclusive")  # or "inclusive", or "linear" by default
    fig.update_layout(xaxis_title="Month", yaxis_title="Production (kWh)")
    st.plotly_chart(fig,use_container_width=True)


    



def plot_cumulative_power_production_plotly(data):
    fig = px.line(data, x='Time', y='cumulative', width=900, height=900)
    fig.update_layout(xaxis_title="Time", yaxis_title="Cumulative Production (kWh)")
    st.plotly_chart(fig,use_container_width=True)

def main():
    

  
    st.markdown("# Solar Production Data" + ':sun_with_face:')
    st.write('You selected:', add_selectbox)
    
    with st.expander("View Data"):
        
        AgGrid(data, wdith=500, height=900)

    # Plotting the data
    st.markdown("# Daily Solar Production" + ':sun_with_face:')
    
    
    
    #plot_power_production(data)
    plot_power_production_plotly(data)


    # Plotting cumulative power production
    st.markdown("# Cumulative Solar Production"  + ':sun_with_face:')
    
    plot_cumulative_power_production_plotly(data)
  

if __name__ == '__main__':
    main()
