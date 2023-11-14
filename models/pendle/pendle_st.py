import streamlit as st
from pendle.core_logic import calculate_var_stETH_APY, compute_seven_day_avg
from pendle.helpers import initialize_session_states, generate_pendle_description, get_response_from_gpt
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Function to run Pendle model logic
def run_pendle_model():
    st.title("Pendle Finance: stETH Underlying APY Simulation")

# Streamlit App Interface
st.title("Pendle Finance: stETH Underlying APY Simulation")

# Sidebar for user input
st.sidebar.image("models/images/pendle.png")
initial_APY_input = st.sidebar.text_input("Starting stETH APY (%)", value="4.20")
initial_APY = float(initial_APY_input)
outlook = st.sidebar.selectbox("stETH Outlook", ["Optimistic", "Neutral", "Pessimistic", "Predict For Me (Coming Soon)"], index=1)
days = st.sidebar.selectbox("Maturity (in days)", [15, 30, 60, 90, 180], index=2)

st.sidebar.write("  \n")
st.sidebar.write("  \n")

methodology = """
**Pendle's stETH Underlying APY Simulation** provides insights into how stETH's APY evolves over time, given the dynamic changes in ETH price, total stETH, and the number of validators in Lido.

Parameter Dynamics:

- **ETH Price**: Depending on the outlook, it fluctuates within certain ranges.
- **Total stETH**: This represents the total amount of stETH and can range between different values based on the chosen outlook.
- **Validators in Lido**: The number of validators can be within different ranges, again based on the selected outlook.
- **APY Calculation**: Starting with the initially inputted APY, for each day, the APY changes based on a formula that factors in the variance in ETH Price, total stETH, and the number of validators.

A **7-Day Moving Average** formula for each day is also computed at the end to comply with the existing Pendle Underlying APY calculation procedure.
"""

# Now you can use the variable in the sidebar markdown function
st.sidebar.markdown(f"### Methodology{methodology}")

st.sidebar.write("  \n")

# Core logic for calculating APYs
CP = 2000  # Current ETH Price
CstETH = 8700000  # Total stETH
CV = 275000  # Current number of validators in Lido
CstETH_APY = initial_APY  # Starting APY

stETH_APYs = [CstETH_APY]
for _ in range(1, days):
    var_stETH_APY_next = calculate_var_stETH_APY(outlook, CP, CstETH, CV)
    CstETH_APY += var_stETH_APY_next
    stETH_APYs.append(CstETH_APY)

# Compute 7-day average of APYs
stETH_APYs_7_day_avg = compute_seven_day_avg(stETH_APYs)

# Visualization of APYs
fig = go.Figure()
fig.add_trace(go.Scatter(x=list(range(1, days + 1)), y=stETH_APYs_7_day_avg, mode='lines', name='stETH APY 7-day Avg'))

y_axis_min = initial_APY - 3.5  # 3.50% below the starting APY
y_axis_max = initial_APY + 3.5  # 3.50% above the starting APY

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

# Display the data table
df_avg = pd.DataFrame({
    'Day': [f"Day {i}" for i in range(1, days + 1)],
    '7-Day Average stETH APY': [f"{val:.4f}%" for val in stETH_APYs_7_day_avg]
})

df_avg = df_avg.iloc[::-1]


data_string = f"Outlook: {outlook}. Time Range: {days} days. {methodology} Data: {df_avg.to_string(index=False)}"

user_question = f"Given the {outlook} outlook over a span of {days} days, provide insights on the progression of the APY values."
pendle_answer = get_response_from_gpt(data_string, user_question)
st.write(pendle_answer)


######################
### SESSION STATE ###
######################


def generate_pendle_description(pendle_model, description):
    # Store the provided description in the session state
    session_state_key = f"description_{pendle_model.replace(' ', '_')}"
    st.session_state[session_state_key] = description

    return description

def initialize_session_states():
    if 'initialized' not in st.session_state:
        st.session_state['initialized'] = True

def get_stored_pendle_description(pendle_model):
    session_state_key = f"description_{pendle_model.replace(' ', '_')}"
    return st.session_state.get(session_state_key, "No description available.")


# Call the function to generate and store the Pendle model description if not already present in session state
pendle_model = "Pendle Finance: stETH Underlying APY Simulation"
pendle_description = pendle_answer

if f'description_{pendle_model.replace(" ", "_")}' not in st.session_state:
    generate_pendle_description(pendle_model, pendle_description)

st.write(st.session_state[f"description_{pendle_model.replace(' ', '_')}"])


#######################


st.table(df_avg.assign(hack='').set_index('hack'))

data_string = f"Outlook: {outlook}. Time Range: {days} days. {methodology} Data: {df_avg.to_string(index=False)}"
data_string += f"\n\n7-Day Average Data:\n{df_avg.to_string(index=False)}"