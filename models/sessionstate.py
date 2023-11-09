import streamlit as st
import sys
sys.path.append('/Users/ASUS/Desktop')
# Assuming openai_integration.py contains the necessary functions to call GPT-3
# Import the functions from the model files
from ./streamlit.py import generate_pendle_description
from ./asymmetrymodel import generate_asymmetry_description


# Function to store the description in Streamlit's session state
def store_model_description_in_state(model_names, description):
    if 'model_descriptions' not in st.session_state:
        st.session_state['model_descriptions'] = {}
    st.session_state['model_descriptions'][model_names] = description

# Function to get the stored description from Streamlit's session state
def get_stored_model_description(model_names):
    if 'model_descriptions' in st.session_state:
        return st.session_state['model_descriptions'].get(model_names)
    return None


def handle_model_interaction(model_name):
    # Check if the description is already stored
    description = get_stored_model_description(model_name)
    
    if description is None:
        # Determine which function to call based on the model_name
        if model_name == "Pendle Finance: stETH Underlying APY Simulation":
            description = generate_pendle_description()
        elif model_name == "Asymmetry Finance: safETH APY Simulation":
            description = generate_asymmetry_description()
        else:
            description = call_gpt3_to_generate_description(model_name)
        
        store_model_description_in_state(model_name, description)
    
    st.write(description)  # Display the description on the page

# Assuming the rest of your script stays the same, update the Streamlit UI components accordingly...

# Model selection
model_names = ["Pendle Finance: stETH Underlying APY Simulation", "Asymmetry Finance: safETH APY Simulation"]
selected_model = st.selectbox("Choose a model to interact with:", model_names)

# Handle model interaction
if st.button(f"Generate Description for {selected_model}"):
    handle_model_interaction(selected_model)

# Generate overview for selected models
if st.button("Generate Strategic Overview"):
    # Here, you would determine which models have been selected by the user
    # For simplicity, we're assuming the user wants an overview of both models
    generate_and_display_overview(model_names)
