import streamlit as st
import polars as pl
from pathlib import Path
import plotly.express as px

st.set_page_config(layout="wide")
st.sidebar.markdown("# Daily production" +  ':chart:')
solar_file = Path(__file__).parent / "solar_production.csv"
# Load data




years = ['2025', '2024', '2023', '2022', '2021']
# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'Select Year',
    ( years ), index=0
)


# read in the data into a lazy frame
data = (
    pl.read_csv(solar_file)
    .with_columns(
        # Convert the Time column to a proper date
        pl.col("Time")
          .str.strptime(pl.Date, format="%Y-%m-%d")
          .alias("Date"),
        
          
    )
    .with_columns (
        year = pl.col("Date").dt.strftime("%Y"),
        month = pl.col("Date").dt.strftime("%B"),
        
    )
    .filter(pl.col("year") == add_selectbox) # filter the data by year selected
    
    .sort("Date")
)


# add a cumulative column
data = data.with_columns(pl.col("Production").cum_sum().alias("cumulative")) # add a cumulative column





# function to plot power function in plotly
def plot_power_production_plotly(data):
    #data['Time'] = pd.to_datetime(data['Time'])  # Convert to datetime format
    #data['Month'] = data['Time'].dt.strftime("%B") # Extract month information
    
    fig = px.box(data, x='month', y='Production', color='month', points="all", 
                 width=900, height=900)
       
    fig.update_traces(quartilemethod="exclusive")  # or "inclusive", or "linear" by default
    fig.update_layout(xaxis_title="Month", yaxis_title="Production (kWh)")
    st.plotly_chart(fig,use_container_width=True)


    
def plot_cumulative_power_production_plotly(data):

    fig = px.line(data, x='Date', y='cumulative', width=900, height=900)
    fig.update_layout(xaxis_title="Date", yaxis_title="Cumulative Production (kWh)")
    st.plotly_chart(fig,use_container_width=True)

def main():
    

  
    st.markdown("# Solar Production Data" + ':sun_with_face:')
    st.write('You selected:', add_selectbox)
    
    plot_power_production_plotly(data)

    plot_cumulative_power_production_plotly(data)
  

if __name__ == '__main__':
    main()
