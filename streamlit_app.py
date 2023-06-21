import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys



solar_file = Path(__file__).parent / "solar_production_2023.csv"
# Load data
data = pd.read_csv(solar_file)
data['cumulative']=data['Production'].cumsum()
# Streamlit app code
def main():
    st.title("Solar Panel Power Production")
    st.write("Solar Production")

    # Display the loaded data
    st.subheader("Solar Panel Data")
    st.dataframe(data)

    # Plotting the data
    st.subheader("Daily Solar Production 2023")
    plot_power_production(data)


    # Plotting cumulative power production
    st.subheader("Cumulative Solar Production 2023")
    plot_cumulative_power_production(data)



    
# Function to plot power production 
def plot_power_production(data):
    data['Time'] = pd.to_datetime(data['Time'])  # Convert to datetime format
    data['Month'] = data['Time'].dt.strftime("%B") # Extract month information
    
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Month', y='Production', data=data)
    sns.swarmplot(x='Month', y='Production', data=data, color="grey")
    

    plt.xlabel('Month')
    plt.ylabel('Power (kWh)')
    plt.title('Solar Panel Power Production')
    plt.legend(title='Month', loc='upper right')
    plt.xticks(rotation=90)  # Rotate x-axis labels by 90 degrees
    plt.grid(True)
    st.pyplot(plt)

# function to plot cumulative power production in seaborn
def plot_cumulative_power_production(data): 
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='Time', y='cumulative', data=data)
    plt.xlabel('Time')
    plt.ylabel('Cumulative Power (kWh)')
    plt.title('Cumulative Solar Panel Power Production')
    plt.grid(True)
    st.pyplot(plt)
  

if __name__ == '__main__':
    main()
