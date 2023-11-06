import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import openai
import random
import os

# Get the API key from the environment variable
openai_api_key = os.environ.get('OPENAI_API_KEY')
if not openai_api_key:
    st.error("Error: API key not found!")
    st.stop()  # Exit the streamlit app with an error
else:
    openai.api_key = openai_api_key


def get_random_value(interval, idx):
    """Generates a random value from an interval based on the given outlook index."""
    lower, upper = interval[idx]
    return random.uniform(lower, upper)

def APY_to_DPY(apy):
    """Converts APY to DPY"""
    return (1 + apy) ** (1/365) - 1

def simulate_icDEY_APY(outlook, time_range):
    # Given outlook, get index
    outlook_map = {"Optimistic": 2, "Neutral": 1, "Pessimistic": 0}
    outlook_idx = outlook_map[outlook]

    Leveraged_cbETH = [(3.8, 4.7), (4.8, 5.7), (5.8, 6.7)]
    Liquidity_Providing = 0.3
    wstETH = [(1.5, 3), (3, 4), (4, 5.5)]
    Daily_Rate = [(0.0025, 0.0125), (0.0126, 0.020), (0.021, 0.040)]

    # Only first APY is random
    first_APY = get_random_value(Leveraged_cbETH, outlook_idx) * Liquidity_Providing * get_random_value(wstETH, outlook_idx)
    APYs = [first_APY]

    for _ in range(1, time_range):
        daily_rate = get_random_value(Daily_Rate, outlook_idx)
        APYs.append(APYs[-1] + daily_rate) 

    return APYs

def simulate_cbETH_APY(time_range):
    cbETH_APY = 3.3
    APYs_cbETH = [cbETH_APY]
    for i in range(1, time_range):
        cbETH_APY += APY_to_DPY(cbETH_APY)
        APYs_cbETH.append(cbETH_APY)
    return APYs_cbETH

def get_response_from_gpt(data_string, question):
    messages = [
        {"role": "system", "content": "You are an analyst. Provide insights based on the given data and the provided methodology. Do not start your response with 'Based on the provided data and methodology' or similar phrasings. Ensure all sentences are complete and end with periods."},
        {"role": "user", "content": f"{data_string}. {question} Please be concise and limit your answer to about four sentences."}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.01,
        max_tokens=150
    )
    return response.choices[0].message['content'].strip()


# Streamlit App
st.title("The Index Coop: icDEY APY Simulation vs cbETH")

st.sidebar.image("indexcoop.png")
st.sidebar.write("")
outlook = st.sidebar.selectbox("icDEY Outlook", ["Optimistic", "Neutral", "Pessimistic"], index=1)
time_range = st.sidebar.selectbox("Time Range (in days)", [15, 30, 60, 90, 180], index=2)
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.markdown("""          
### Methodology

- **icDEY** is derived from randomly selected values from predefined ranges for Leveraged_cbETH and wstETH, both dependent on the outlook (optimistic, neutral, and pessimistic). The initial APY is a product of this multiplier and a constant liquidity providing rate (0.3% Uniswap V3 standard). For each subsequent day, a random daily rate is added to the previous day's APY, which is also dependent on the outlook.

- **cbETH** starts with an initial APY of 3.3%. For each subsequent day, a compounded daily percentage yield is added to the previous day's APY.
                    
Learn more on The Index Coop [here](https://indexcoop.com/).

Visit the [source code](https://github.com/bmvicente/tokensight/blob/main/icDEY.py).                    
""")

st.sidebar.write("")
st.sidebar.write("")

icDEY_APYs = simulate_icDEY_APY(outlook, time_range)
cbETH_APYs = simulate_cbETH_APY(time_range)

fig = go.Figure()

fig.add_trace(go.Scatter(x=list(range(1, time_range+1)), 
                         y=icDEY_APYs, 
                         mode='lines', 
                         name='icDEY APY', 
                         line=dict(color="Black")))

fig.add_trace(go.Scatter(x=list(range(1, time_range+1)), 
                         y=cbETH_APYs, 
                         mode='lines', 
                         name='cbETH APY', 
                         line=dict(color="Blue")))



#fig.update_layout(
#    xaxis_title='Days',
#    yaxis_title='APY',
#    hovermode='x unified',
#    yaxis=dict(range=[0, max(icDEY_APYs + cbETH_APYs) + 5], tickvals=list(range(0, int(max(icDEY_APYs + cbETH_APYs) + 5), 5)), ticktext=[f"{i}%" for i in range(0, int(max(icDEY_APYs + cbETH_APYs) + 5), 5)]))

fig.update_layout(
    xaxis_title='Days',
    yaxis_title='APY',
    hovermode='x unified',
    yaxis=dict(range=[0, 17], tickvals=list(range(0, 18, 5)), ticktext=[f"{i}%" for i in range(0, 18, 5)]))


st.plotly_chart(fig)

df = pd.DataFrame({
    'Days': [f"Day {i}" for i in range(1, time_range+1)],
    'icDEY APY': [f"{val:.4f}%" for val in icDEY_APYs],
    'cbETH APY': [f"{val:.4f}%" for val in cbETH_APYs]
})

# Convert our dataframe to a string
data_string = f"Outlook: {outlook}. Time Range: {time_range} days. Methodology: icDEY is derived from randomly selected values from predefined ranges for Leveraged_cbETH and Pendle_stETH_Boosted_APY, dependent on the outlook. The initial APY multiplies this with a constant liquidity providing rate. Subsequent days add a random daily rate to the previous APY. cbETH starts at 3.3% APY, with a compounded yield added each day. Data: {df.to_string(index=False)}"

# Ask the user for a question
user_question = f"Given the {outlook} outlook over a span of {time_range} days, provide insights on the progression of the APYs values."

# Get the answer from GPT and display it
answer = get_response_from_gpt(data_string, user_question)
st.write(answer)

st.table(df.set_index('Days'))