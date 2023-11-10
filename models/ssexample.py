import streamlit as st
import openai
import os
from pendle.helpers import get_stored_pendle_description
from asymmetry.core_logic import get_stored_asymmetry_description
#from models.indexcoop.core_logic import get_stored_indexcoop_description


# Setup API key for OpenAI
openai_api_key = os.environ.get('OPENAI_API_KEY')
if openai_api_key:
    openai.api_key = openai_api_key

# Define a list of available simulation models
available_models = ['Pendle', 'Asymmetry']

# Predefined descriptions for each model (replace these with actual descriptions)
model_descriptions = {
    'Pendle': get_stored_pendle_description("Pendle"),
    'Asymmetry': get_stored_asymmetry_description("Asymmetry")
    #'Index Coop': get_stored_indexcoop_description("indexcoop_model")
}

# Function to call GPT-3 for suggestions
def call_gpt3_for_suggestions(combined_description):
    prompt = f"Based on the following combined strategy: {combined_description}. What would be the best path forward?"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Function to generate the combined strategy text
def generate_strategy():
    if len(st.session_state.selected_models) < 2:
        st.error("Please select at least two simulation models.")
        return
    
    combined_description = " ".join(model_descriptions[model] for model in st.session_state.selected_models)
    combined_strategy = f"The combined strategy integrates {', '.join(st.session_state.selected_models)} with an approach based on: {combined_description}"

    st.session_state['strategy_generated'] = True
    st.session_state['combined_strategy'] = combined_strategy
    # Get suggestions from GPT-3 based on the combined strategy
    st.session_state['gpt_suggestions'] = call_gpt3_for_suggestions(combined_description)

# Initialize session state variables
if 'selected_models' not in st.session_state:
    st.session_state['selected_models'] = []

if 'strategy_generated' not in st.session_state:
    st.session_state['strategy_generated'] = False

if 'combined_strategy' not in st.session_state:
    st.session_state['combined_strategy'] = ''

if 'gpt_suggestions' not in st.session_state:
    st.session_state['gpt_suggestions'] = ''

# UI Components
with st.form(key='strategy_form'):
    st.session_state.selected_models = st.multiselect(
        'Select Simulation Models (Choose 2 or more):',
        available_models,
        st.session_state.selected_models
    )
    
    submit_button = st.form_submit_button(label='Generate Strategy', on_click=generate_strategy)

# Display the combined strategy and GPT-3 suggestions
if st.session_state.strategy_generated:
    st.write("### Combined Strategy:")
    st.write(st.session_state.combined_strategy)
    st.write("### GPT-3 Suggestions:")
    st.write(st.session_state.gpt_suggestions)
