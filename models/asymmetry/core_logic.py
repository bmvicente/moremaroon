import random
import os
import openai
import streamlit as st

# Setup API key for OpenAI
openai_api_key = os.environ.get('OPENAI_API_KEY')
if openai_api_key:
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
        APY_next = total_apy_for_day * daily_rate
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


####### SESSION STATE #######

def call_gpt3_to_generate_asymmetry_description(asymmetry_model):
    # Ensure you have the API key set before calling this function
    if not openai_api_key:
        raise ValueError("OpenAI API key not found!")

    # Actual call to OpenAI's API to generate a description
    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # Or whichever model you're using
            prompt=f"Write a concise model description for a financial model named {asymmetry_model}.",
            temperature=0.7,
            max_tokens=100
        )
        # Extracting the text from the response
        description = response.choices[0].text.strip()
        return description
    except Exception as e:
        raise Exception(f"An error occurred while generating the description: {str(e)}")
    
def generate_asymmetry_description(asymmetry_model):
    # Call GPT-3 to generate a description
    asymmetry_description = call_gpt3_to_generate_asymmetry_description(asymmetry_model)
    
    # Store the description in the session state
    session_state_key = f"description_{asymmetry_model.replace(' ', '_')}"
    st.session_state[session_state_key] = asymmetry_description
    
    return asymmetry_description


def initialize_session_states():
    if 'initialized' not in st.session_state:
        st.session_state['initialized'] = True

def get_stored_asymmetry_description(asymmetry_model):
    session_state_key = f"description_{asymmetry_model.replace(' ', '_')}"
    return st.session_state.get(session_state_key, "No description available.")