import streamlit as st
from core_logic import (
    calculate_weighted_average_APY,
    compute_seven_day_avg,
    get_response_from_gpt,
    initialize_session_states,
    generate_asymmetry_description
)
from plot import create_apy_plot
import pandas as pd

# Initialize session states if not already set
initialize_session_states()

# Streamlit App Interface
st.title("Asymmetry Finance: safETH APY Simulation")

# Sidebar configuration and user input
st.sidebar.image("models/images/asymmetry.png")  # Assuming 'asymmetry.png' is in the correct directory
st.sidebar.write("  \n")
initial_APY_input = st.sidebar.text_input("Starting safETH APY (%)", value="4.20")
initial_APY = float(initial_APY_input)
outlook = st.sidebar.selectbox("safETH Outlook", ["Optimistic", "Neutral", "Pessimistic"], index=1)
days = st.sidebar.selectbox("Time Range (in days)", [15, 30, 60, 90, 180], index=2)

# Methodology section in the sidebar
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

# Main app logic
APYs = calculate_weighted_average_APY(outlook, days, initial_APY)
APYs_7_day_avg = compute_seven_day_avg(APYs)

# Plot the APYs using Plotly
fig = create_apy_plot(days, APYs_7_day_avg, initial_APY)
st.plotly_chart(fig)

# Display the data table
df = pd.DataFrame({
    'Day': [f"Day {i}" for i in range(1, days+1)],
    '7-Day Weighted Average APY': [f"{val:.4f}%" for val in APYs_7_day_avg]
})

df = df.iloc[::-1]

st.table(df.assign(hack='').set_index('hack'))

# Generate and display data insights using GPT-3
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

user_question = f"Given the {outlook} outlook over a span of {days} days, provide insights on the progression of the APY values."
answer = get_response_from_gpt(data_string, user_question)
st.write(answer)

# Call to generate description if not already in session state
asymmetry_model = "Asymmetry Finance: safETH APY Simulation"
if f'description_{asymmetry_model.replace(" ", "_")}' not in st.session_state:
    description = generate_asymmetry_description(asymmetry_model)
    st.session_state[f'description_{asymmetry_model.replace(" ", "_")}'] = description

# Optionally display the stored description
st.write(st.session_state.get(f'description_{asymmetry_model.replace(" ", "_")}', 'No description available.'))