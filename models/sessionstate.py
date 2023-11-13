import streamlit as st
import sys
sys.path.append('/Users/ASUS/Desktop')
from pendle.streamlit import generate_pendle_description, initialize_session_states
from asymmetry.streamlit import generate_asymmetry_description, initialize_session_states

def store_model_description_in_state(model_names, description):
    if 'model_descriptions' not in st.session_state:
        st.session_state['model_descriptions'] = {}
    st.session_state['model_descriptions'][model_names] = description

def get_stored_model_description(model_names):
    if 'model_descriptions' in st.session_state:
        return st.session_state['model_descriptions'].get(model_names)
    return None

def handle_model_interaction(model_name):
    description = get_stored_model_description(model_name)
    if description is None:
        if model_name == "Pendle Finance: stETH Underlying APY Simulation":
            description = generate_pendle_description()
        elif model_name == "Asymmetry Finance: safETH APY Simulation":
            description = generate_asymmetry_description()
        else:
            description = "Description not available for this model."
        store_model_description_in_state(model_name, description)
    st.write(description)

# Model selection interface
model_names = ["Pendle Finance: stETH Underlying APY Simulation", "Asymmetry Finance: safETH APY Simulation"]
selected_model = st.selectbox("Choose a model to interact with:", model_names)

# Interaction button
if st.button(f"Generate Description for {selected_model}"):
    handle_model_interaction(selected_model)

def generate_and_display_overview(model_names):
    descriptions = [get_stored_model_description(model) for model in model_names]
    valid_descriptions = [desc for desc in descriptions if desc is not None]
    if valid_descriptions:
        combined_description = ' '.join(valid_descriptions)
        st.write("Strategic Overview:")
        st.write(combined_description)
    else:
        st.write("No descriptions available for the selected models.")
