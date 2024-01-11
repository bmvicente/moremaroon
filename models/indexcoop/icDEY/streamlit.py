import streamlit as st
import pandas as pd
from icDEY_logic import simulate_icDEY_APY, simulate_cbETH_APY
from plot import create_plot

# Streamlit App Configuration
st.title("The Index Coop: icDEY APY Simulation vs cbETH")

st.sidebar.image("models/images/indexcoop.png")
st.sidebar.write("")
outlook = st.sidebar.selectbox("icDEY Outlook", ["Optimistic", "Neutral", "Pessimistic", "Predict For Me (Coming Soon)"], index=1)
time_range = st.sidebar.selectbox("Time Range (in days)", [15, 30, 60, 90, 180], index=2)

# Sidebar Methodology and Links
st.sidebar.markdown("""          
### Methodology

- **icDEY** is derived from randomly selected values from the below predefined ranges for Leveraged_cbETH and wstETH, dependent on the outlook. The initial APY multiplies this with a constant liquidity providing rate. Subsequent days add a random daily rate to the previous APY:
                    ***Leveraged cbETH range*** = [(3.8, 4.7), (4.8, 5.7), (5.8, 6.7)] | 
    ***Liquidity Providing range*** = 0.3 | 
    ***wstETH range*** = [(1.5, 3), (3, 4), (4, 5.5)] | 
    ***Daily Compounding Rate range*** = [(0.0025, 0.0125), (0.0126, 0.020), (0.021, 0.040)]

- **cbETH** starts with an initial APY of 3.3%, with a compounded yield added each day.

Learn more on The Index Coop [here](https://indexcoop.com/).
Visit the [source code](https://github.com/bmvicente/tokensight/blob/main/icDEY.py).                    
""")

# Simulation and Plotting
icDEY_APYs = simulate_icDEY_APY(outlook, time_range)
cbETH_APYs = simulate_cbETH_APY(time_range)
fig = create_plot(icDEY_APYs, cbETH_APYs, time_range)
st.plotly_chart(fig)

# Dataframe for display
df = pd.DataFrame({
    'Days': [f"Day {i}" for i in range(1, time_range+1)],
    'icDEY APY': [f"{val:.4f}%" for val in icDEY_APYs],
    'cbETH APY': [f"{val:.4f}%" for val in cbETH_APYs]
})

df = df.iloc[::-1]

# Displaying the Data Table
st.table(df.set_index('Days'))