import os
import openai
import streamlit as st


# Setup API key for OpenAI
openai_api_key = os.environ.get('OPENAI_API_KEY')
if openai_api_key:
    openai.api_key = openai_api_key

def get_response_from_gpt(data_string, question):
    messages = [
        {"role": "system", "content": "You are an analyst. Provide insights based on the given data and the provided methodology. Do not start your response with 'Based on the provided data and methodology' or similar phrasings. Ensure all sentences are complete and end with periods."},
        {"role": "user", "content": f"{data_string}. {question} Please be concise and limit your answer to about four sentences."}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.01,
        max_tokens=250
    )
    return response.choices[0].message['content'].strip()
    
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
