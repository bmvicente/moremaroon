import streamlit as st
import sys
sys.path.append('/Users/ASUS/Desktop')
# Assuming openai_integration.py contains the necessary functions to call GPT-3
# Import the functions from the model files
from pendle.streamlit import generate_pendle_description, call_gpt3_to_generate_pendle_description
#from pendle.helpers import generate_pendle_description, call_gpt3_to_generate_pendle_description, initialize_session_states
from asymmetry.streamlit import generate_asymmetry_description, call_gpt3_to_generate_asymmetry_description
#from asymmetry.core_logic import call_gpt3_to_generate_asymmetry_description, generate_asymmetry_description, initialize_session_states
#from indexcoop.streamlit import generate_indexcoop_description, call_gpt3_to_generate_indexcoop_description
#from eigenlayer.streamlit import generate_eigenlayer_description, call_gpt3_to_generate_eigenlayer_description


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
            description = call_gpt3_to_generate_pendle_description()
        elif model_name == "Asymmetry Finance: safETH APY Simulation":
            description = call_gpt3_to_generate_asymmetry_description()
        #elif model_name == "Index Coop":
        #    description = call_gpt3_to_generate_indexcoop_description()
        #elif model_name == "Eigenlayer":
        #    description = call_gpt3_to_generate_eigenlayer_description()
        else:
            return None
        
        store_model_description_in_state(model_name, description)
    
    if description is not None:
        st.write(description)  # Display the description on the page


# Model selection
model_names = ["Pendle Finance: stETH Underlying APY Simulation", "Asymmetry Finance: safETH APY Simulation"]
selected_model = st.selectbox("Choose a model to interact with:", model_names)

# Handle model interaction
if st.button(f"Generate Description for {selected_model}"):
    handle_model_interaction(selected_model)

def generate_and_display_overview(model_names):
    # Check if descriptions for the models are stored, and if so, concatenate them
    descriptions = [get_stored_model_description(model) for model in model_names]
    
    # Filter out None values in case some descriptions are not found
    valid_descriptions = [desc for desc in descriptions if desc is not None]

    if valid_descriptions:
        # Combine the descriptions and display
        combined_description = ' '.join(valid_descriptions)
        st.write("Strategic Overview:")
        st.write(combined_description)  # Display the combined description on the page
    else:
        st.write("No descriptions available for the selected models.")
