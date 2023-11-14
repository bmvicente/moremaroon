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

