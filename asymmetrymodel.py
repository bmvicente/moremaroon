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

def calculate_weighted_average_APY(outlook, time_range, initial_APY):
    outlook_map = {
        "Optimistic": 2,
        "Neutral": 1,
        "Pessimistic": 0
    }
    outlook_idx = outlook_map[outlook]

    tokens = {
        "wstETH": (0.17, [(2.00, 3.00), (3.00, 4.00), (4.00, 6.00)]),
        "rETH": (0.21, [(1.75, 2.75), (2.75, 3.50), (3.50, 5.50)]),
        "sfrxETH": (0.21, [(2.75, 3.50), (3.50, 4.50), (4.50, 6.00)]),
        "ankrETH": (0.05, [(5.00, 6.50), (6.50, 7.50), (7.50, 9.00)]),
        "swETH": (0.21, [(2.75, 3.50), (3.50, 4.50), (4.50, 6.00)]),
        "stafi": (0.15, [(2.00, 3.00), (3.00, 4.00), (4.00, 6.00)])
    }

    Daily_Rate = [(-0.02, -0.005),(-0.005,0.005),(0.005, 0.02)]

    APYs = []

    # Calculate the initial APY (for day 1)
    APYs = [initial_APY]  # Set the starting value of the APYs list to the provided initial_APY


    # Adjust the APYs using the daily rate for each subsequent day
    for _ in range(1, time_range):
        daily_rate = get_random_value(Daily_Rate[outlook_idx])
        
        # Calculate token-wise APYs for the current day
        token_APYs = []
        for _, (weight, apy_ranges) in tokens.items():
            token_apy = get_random_value(apy_ranges[outlook_idx])
            token_APYs.append(token_apy * weight)
        
        # Sum the weighted token APYs to get the overall APY for the day
        total_apy_for_day = sum(token_APYs)
        
        # Adjust this with the daily rate
        APY_next = total_apy_for_day + daily_rate
        APYs.append(APY_next)

    return APYs

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
    
def compute_seven_day_avg(apy_values):
    averages = []
    for idx, value in enumerate(apy_values):
        if idx < 6:  # For the first 6 days, average with all previous values including the current one
            averages.append(sum(apy_values[:idx+1]) / (idx+1))
        else:  # From the 7th day onward, compute the 7-day rolling average
            averages.append(sum(apy_values[idx-6:idx+1]) / 7)
    return averages

def generate_asymmetry_description(model_name):
    # Call GPT-3 to generate a description
    asymmetry_description = call_gpt3_to_generate_description(model_name)
    
    # Store the description in the session state
    session_state_key = f"description_{model_name.replace(' ', '_')}"
    st.session_state[session_state_key] = asymmetry_description
    
    return asymmetry_description

def call_gpt3_to_generate_description(model_name):
    # Here you'd include your actual code to call GPT-3
    # For example:
    response = openai.Completion.create(
        model="text-davinci-003",  # Specify the model you are using
        prompt=f"Write a concise model description for a financial model named {model_name}.",
        temperature=0.7,
        max_tokens=100
    )
    return response.choices[0].text.strip()

# Streamlit App starts here
st.title("Asymmetry Finance: safETH APY Simulation")


# Image
st.sidebar.image("asymmetry.png")
st.sidebar.write("  \n")
st.sidebar.write("  \n")

# Get initial APY input from the user
initial_APY_input = st.sidebar.text_input("Starting safETH APY (%)", value="4.20")
initial_APY = float(initial_APY_input)
outlook = st.sidebar.selectbox("safETH Outlook", ["Optimistic", "Neutral", "Pessimistic"], index=1)
days = st.sidebar.selectbox("Time Range (in days)", [15, 30, 60, 90, 180], index=2)

st.sidebar.write("  \n")
st.sidebar.write("  \n")
st.sidebar.markdown("""          
### Methodology
**Asymmetry Finance's safETH APY Simulation** encompasses the following calculations:

- **Token Weighted APYs**: safETH's APY is a weighted sum of individual token APYs. Each token is assigned a weight, and its APY range varies based on the chosen outlook (Optimistic, Neutral, or Pessimistic). These token APYs are derived from a randomized selection within their respective ranges:
17% wstETH, 21% rETH, 21% sfrxETH,  5% ankrETH, 21% swETH, 15% stafi.
Starting APY: The simulation begins with the inputted APY. For each subsequent day, the APY is a weighted average based on the randomized token APYs and their assigned weights.

- **7-Day Rolling Average**: From the seventh day onward, a 7-day rolling average is computed. For the first six days, the average is computed based on all previous values, including the current day's value.

Once the above APY values are calculated and presented in the plot an analysis is provided based on the progression of the weighted average APY values throughout the days.

Learn more on Asymmetry Finance [here](https://www.asymmetry.finance/).                    
""")

st.sidebar.write("  \n")



# Call the function to generate and store the description
model_name = "Asymmetry Finance: safETH APY Simulation"
if f'description_{model_name.replace(" ", "_")}' not in st.session_state:
    generate_asymmetry_description(model_name)



# Initial APY (assuming the same starting value as before)
#initial_APY = 3.70  # Starting APY

APYs = calculate_weighted_average_APY(outlook, days, initial_APY)
APYs_7_day_avg = compute_seven_day_avg(APYs)

# Calculate the y-axis limits based on the starting APY
y_axis_min = initial_APY - 2.5  # 2% below the starting APY
y_axis_max = initial_APY + 2.5  # 2% above the starting APY

# Create and display the visualization
fig = go.Figure()
fig.add_trace(go.Scatter(x=list(range(1, days+1)), y=APYs_7_day_avg, mode='lines', name='safETH APY'))
fig.update_layout(
    hovermode = 'x unified',
    xaxis_title="Days",
    yaxis_title="APY",
    showlegend=True
)
fig.update_yaxes(
    range=[y_axis_min, y_axis_max],
    dtick=0.05,
    tickvals=[val for val in np.linspace(y_axis_min, y_axis_max, 10)],
    ticktext=[f"{val:.2f}%" for val in np.linspace(y_axis_min, y_axis_max, 10)]
)
st.plotly_chart(fig)

# Convert the APY values into a DataFrame
df = pd.DataFrame({
    'Day': [f"Day {i}" for i in range(1, days+1)],
    '7-Day Weighted Average APY': [f"{val:.4f}%" for val in APYs_7_day_avg]
})

# Convert our dataframe to a string
data_string = f"""
Outlook: {outlook}.
Number of Days: {days}.

Methodology:
Asymmetry Finance's safETH APY Simulation encompasses the following calculations:
- Token Weighted APYs: safETH's APY is derived from randomly selected values within predefined ranges for tokens (wstETH, rETH, sfrxETH, ankrETH, swETH, stafi), dependent on the outlook.
- The simulation starts with a constant APY of 3.70%. Subsequent days are based on the randomized token APYs.
- From the seventh day onwards, a 7-day rolling average is computed. 

Data:
{df.to_string(index=False)}
"""

# Ask the user for a question
user_question = f"Given the {outlook} outlook over a span of {days} days, provide insights on the progression of the APY values."

# Get the answer from GPT and display it
answer = get_response_from_gpt(data_string, user_question)
st.write(answer)

# Display the data table
st.table(df.assign(hack='').set_index('hack'))

