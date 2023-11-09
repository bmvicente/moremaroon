import streamlit as st
import random
import numpy as np
import pandas as pd
import openai
import plotly.graph_objects as go
import os

# Get the API key from the environment variable
openai_api_key = os.environ.get('OPENAI_API_KEY')
if not openai_api_key:
    st.error("Error: API key not found!")
    st.stop()  # Exit the streamlit app with an error
else:
    openai.api_key = openai_api_key

def get_random_value(interval):
    """Generates a random value from an interval."""
    lower, upper = interval
    return random.uniform(lower, upper)

def calculate_var_stETH_APY(outlook, CP, CstETH, CV):
    outlook_map = {
        "Optimistic": 0,
        "Neutral": 1,
        "Pessimistic": 2
    }

    FP_ranges = [(1300.00, 1550.00), (1550.00, 1750.00), (1750.00, 2000.00)]
    FstETH_ranges = [(2.00, 3.25), (3.25, 4.25), (4.25, 5.50)]
    FV_ranges = [(780000, 820000), (820000, 850000), (850000, 890000)]

    outlook_idx = outlook_map[outlook]

    FP = get_random_value(FP_ranges[outlook_idx])
    FstETH = get_random_value(FstETH_ranges[outlook_idx])
    FV = get_random_value(FV_ranges[outlook_idx])

    var_stETH_APY_next = (1/5)*((FP-CP)/CP) * (1/2)*((FstETH-CstETH)/CstETH) * (3/10)*((FV-CV)/CV)
    return var_stETH_APY_next

# Commented out the GPT-related function
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

# Add the 7-day moving average function from the previous script
def compute_seven_day_avg(apy_values):
    averages = []
    for idx, value in enumerate(apy_values):
        if idx < 6:  # For the first 6 days, average with all previous values including the current one
            averages.append(sum(apy_values[:idx+1]) / (idx+1))
        else:  # From the 7th day onward, compute the 7-day rolling average
            averages.append(sum(apy_values[idx-6:idx+1]) / 7)
    return averages

def generate_pendle_description(pendle_model):
    # Call GPT-3 to generate a description
    pendle_description = call_gpt3_to_generate_description(pendle_model)
    
    # Store the description in the session state
    session_state_key = f"description_{pendle_model.replace(' ', '_')}"
    st.session_state[session_state_key] = pendle_description
    
    return pendle_description

def call_gpt3_to_generate_description(pendle_model):
    # Here you'd include your actual code to call GPT-3
    # For example:
    response = openai.Completion.create(
        model="text-davinci-003",  # Specify the model you are using
        prompt=f"Write a concise model description for a financial model named {pendle_model}.",
        temperature=0.7,
        max_tokens=100
    )
    return response.choices[0].text.strip()

# Streamlit App
st.title("Pendle Finance: stETH Underlying APY Simulation")

# Image
st.sidebar.image("models/images/pendle.png")
st.sidebar.write("  \n")

initial_APY_input = st.sidebar.text_input("Starting stETH APY(%)", value="4.20")
initial_APY = float(initial_APY_input)

outlook = st.sidebar.selectbox("stETH Outlook", ["Optimistic", "Neutral", "Pessimistic"], index=1)
days = st.sidebar.selectbox("Maturity (in days)", [15, 30, 60, 90, 180], index=2)

st.sidebar.write("  \n")
st.sidebar.write("  \n")

hide_st_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.sidebar.markdown("""          
### Methodology
**Pendle's stETH Underlying APY Simulation** provides insights into how stETH's APY evolves over time, given the dynamic changes in ETH price, total stETH, and the number of validators in Lido.

Parameter Dynamics:

- **ETH Price**: Depending on the outlook, it fluctuates within certain ranges.
- **Total stETH**: This represents the total amount of stETH and can range between different values based on the chosen outlook.
- **Validators in Lido**: The number of validators can be within different ranges, again based on the selected outlook.
- **APY Calculation**: Starting with the initially inputted APY, for each day, the APY changes based on a formula that factors in the variance in ETH Price, total stETH, and the number of validators.

A **7-Day Moving Average** formula for each day is also computed at the end to comply with the existing Pendle Underlying APY calculation procedure.                    

Learn more on Pendle [here](https://www.pendle.finance/) and on Pendle Yield Trading [here](https://app.pendle.finance/trade/education/learn?level=4).                    
""")

st.sidebar.write("  \n")


# Call the function to generate and store the description
pendle_model = "Pendle Finance: stETH Underlying APY Simulation"
if f'description_{pendle_model.replace(" ", "_")}' not in st.session_state:
    generate_pendle_description(pendle_model)


# Initial values for the parameters
CP = 1650 #Current ETH Price
CstETH = 8700000 #Total stETH
CV = 275000 #Current number of validators in Lido
CstETH_APY = initial_APY  # Starting APY

stETH_APYs = [CstETH_APY]
for _ in range(1, days):
    var_stETH_APY_next = calculate_var_stETH_APY(outlook, CP, CstETH, CV)
    CstETH_APY += var_stETH_APY_next
    stETH_APYs.append(CstETH_APY)


y_axis_min = initial_APY - 5  # 5% below the starting APY
y_axis_max = initial_APY + 5  # 5% above the starting APY

stETH_APYs_7_day_avg = compute_seven_day_avg(stETH_APYs)


# Create and display the visualization
fig = go.Figure()
fig.add_trace(go.Scatter(x=list(range(1, days+1)), y=stETH_APYs_7_day_avg, mode='lines', name='stETH APY 7-day Avg'))

y_axis_min = initial_APY - 2  # 2% below the starting APY
y_axis_max = initial_APY + 2  # 2% above the starting APY

fig.update_layout(
    hovermode = 'x unified',
    xaxis_title="Days",
    yaxis_title="APY",
    showlegend=True,
    yaxis=dict(range=[y_axis_min, y_axis_max])  # set the y-axis range
)
fig.update_yaxes(
    dtick=0.05,
    tickvals=[val for val in np.linspace(y_axis_min, y_axis_max, 10)],
    ticktext=[f"{val:.2f}%" for val in np.linspace(y_axis_min, y_axis_max, 10)]
)

st.plotly_chart(fig)

df_avg = pd.DataFrame({
    'Day': [f"Day {i}" for i in range(1, days+1)],
    '7-Day Average stETH APY': [f"{val:.4f}%" for val in stETH_APYs_7_day_avg]
})

# Convert our dataframe to a string
methodology = """
**Pendle's stETH Underlying APY Simulation** provides insights into how stETH's APY evolves over time, given the dynamic changes in ETH price, total stETH, and the number of validators in Lido.

Parameter Dynamics:

- **ETH Price**: Depending on the outlook, it fluctuates within certain ranges.
- **Total stETH**: This represents the total amount of stETH and can range between different values based on the chosen outlook.
- **Validators in Lido**: The number of validators can be within different ranges, again based on the selected outlook.
- **APY Calculation**: Starting with an initial APY of 3.50%, for each day, the APY changes based on a formula that factors in the variance in ETH Price, total stETH, and the number of validators.
"""
data_string = f"Outlook: {outlook}. Time Range: {days} days. {methodology} Data: {df_avg.to_string(index=False)}"

data_string += f"\n\n7-Day Average Data:\n{df_avg.to_string(index=False)}"

# Commented out the parts related to getting answer from GPT and displaying it
#Ask the user for a question
user_question = f"Given the {outlook} outlook over a span of {days} days, provide insights on the progression of the APY values."

#Get the answer from GPT and display it
answer = get_response_from_gpt(data_string, user_question)
append_paragraph = "\n\nWhen in a Yield Trading strategy on Pendle, if the initial Underlying stETH APY is lower than the Implied stETH APY but surpasses it at maturity, you'll likely profit. Otherwise, your investment is likely to incur a loss."

answer += append_paragraph

st.write(answer)

# Display the data table
st.table(df_avg.assign(hack='').set_index('hack'))