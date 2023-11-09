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
        max_tokens=150
    )
    return response.choices[0].message['content'].strip()

def generate_pendle_description(pendle_model):
    # Call GPT-3 to generate a description
    pendle_description = call_gpt3_to_generate_pendle_description(pendle_model)
    
    # Store the description in the session state
    session_state_key = f"description_{pendle_model.replace(' ', '_')}"
    st.session_state[session_state_key] = pendle_description
    
    return pendle_description

def call_gpt3_to_generate_pendle_description(pendle_model):
    # Ensure you have the API key set before calling this function
    if not openai_api_key:
        raise ValueError("OpenAI API key not found!")

    # Actual call to OpenAI's API to generate a description
    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # Or whichever model you're using
            prompt=f"Write a concise model description for a financial model named {pendle_model}.",
            temperature=0.7,
            max_tokens=100
        )
        # Extracting the text from the response
        description = response.choices[0].text.strip()
        return description
    except Exception as e:
        raise Exception(f"An error occurred while generating the description: {str(e)}")
    

def generate_pendle_description(model_name):

    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # Or whichever GPT model you're using
            prompt=f"Write a concise description for a financial model named {model_name}.",
            temperature=0.7,
            max_tokens=100
        )
        description = response.choices[0].text.strip()
        return description
    except openai.error.OpenAIError as e:
        st.error(f"An error occurred while generating the description: {str(e)}")
        return None

def initialize_session_states():
    if 'initialized' not in st.session_state:
        st.session_state['initialized'] = True
