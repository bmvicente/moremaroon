import streamlit as st
from core_logic import calculate_apy
from plot import create_apy_plot

st.title("EigenLayer: LST Restaking APY Simulation")

# Sidebar with Inputs
st.sidebar.image("images/eigenlayers.jpg")
starting_apy_percentage = st.sidebar.slider('Starting APY (%):', min_value=0.0, max_value=10.0, value=0.0, step=0.1)
r_annual_percentage = st.sidebar.slider('Annual interest rate (%):', min_value=0.0, max_value=10.0, value=5.0, step=0.1)
r_annual = r_annual_percentage / 100
timeframe_days = st.sidebar.selectbox('Time range (in days):', [15, 30, 60, 90, 180], index=2)
n = st.sidebar.number_input('Number of restaking events per Time Range chosen:', min_value=1, value=5)
starting_apy = starting_apy_percentage / 100

st.sidebar.write("  \n")
st.sidebar.write("  \n")
st.sidebar.markdown("""
### Methodology
**EigenLayer's LST Restaking APY Simulation** encompasses the following calculations:

Learn more on EigenLayer [here](https://www.eigenlayer.xyz/).
""")

df = calculate_apy(starting_apy, r_annual, timeframe_days, n)
fig = create_apy_plot(df)

# Displaying Line Chart
st.plotly_chart(fig)

# Displaying DataFrame
st.write(df)
