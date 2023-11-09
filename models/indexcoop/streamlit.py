import streamlit as st
import pandas as pd
from core_logic import simulate_icDEY_APY, simulate_cbETH_APY, get_response_from_gpt
from plot import create_plot

# Streamlit App Configuration
st.title("The Index Coop: icDEY APY Simulation vs cbETH")

st.sidebar.image("models/images/indexcoop.png")
st.sidebar.write("")
outlook = st.sidebar.selectbox("icDEY Outlook", ["Optimistic", "Neutral", "Pessimistic"], index=1)
time_range = st.sidebar.selectbox("Time Range (in days)", [15, 30, 60, 90, 180], index=2)

# Sidebar Methodology and Links
st.sidebar.markdown("""          
### Methodology

- **icDEY** is derived from randomly selected values from predefined ranges for Leveraged_cbETH and wstETH, dependent on the outlook. The initial APY multiplies this with a constant liquidity providing rate. Subsequent days add a random daily rate to the previous APY.
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

# GPT-3 Integration for Analysis
data_string = f"Outlook: {outlook}. Time Range: {time_range} days. Data: {df.to_string(index=False)}"
user_question = f"Given the {outlook} outlook over a span of {time_range} days, provide insights on the progression of the APYs values."
answer = get_response_from_gpt(data_string, user_question)
st.write(answer)

# Displaying the Data Table
st.table(df.set_index('Days'))