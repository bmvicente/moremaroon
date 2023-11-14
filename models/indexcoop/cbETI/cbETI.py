import openpyxl
import numpy as np
import random
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import openai
import os
import requests
from io import BytesIO

# Get the API key from the environment variable
#openai_api_key = os.environ.get('OPENAI_API_KEY')
#if not openai_api_key:
#    st.error("Error: API key not found!")
#    st.stop()  # Exit the streamlit app with an error
#else:
#    openai.api_key = openai_api_key


def read_xlsx_from_github(raw_url):
    response = requests.get(raw_url)
    response.raise_for_status()  # Raise an error if the request failed

    # Use BytesIO to convert the content into a file-like object so openpyxl can read it
    workbook = openpyxl.load_workbook(BytesIO(response.content))
    
    sheet = workbook.active  # Assuming we're reading the first sheet

    headers = []
    data = []
    for index, row in enumerate(sheet.iter_rows(values_only=True)):
        if index == 0:  # If it's the first row, treat it as headers
            headers = list(row)
        else:
            data.append(list(row))

    return headers, data

# Raw URLs from GitHub
url1 = "https://raw.githubusercontent.com/bmvicente/tokensight/main/Moving%20Average%20Pairs.xlsx"
url2 = "https://raw.githubusercontent.com/bmvicente/tokensight/main/DF%20%26%20NF.xlsx"

# Read the xlsx files from GitHub and store headers and data in variables
headers_moving_average_pairs, data_moving_average_pairs = read_xlsx_from_github(url1)
headers_df_nf, data_df_nf = read_xlsx_from_github(url2)

print("Headers from Moving Average Pairs.xlsx:")
print(headers_moving_average_pairs)
print("\nData from Moving Average Pairs.xlsx:")
print(data_moving_average_pairs)

print("\nHeaders from DF & NF.xlsx:")
print(headers_df_nf)
print("\nData from DF & NF.xlsx:")
print(data_df_nf)



#UI randomized

def randomize_underlying_index():
    # Your logic here...
    return random.uniform(-20, 20)  # This is just a placeholder. Adjust the logic as needed.

# Calculate the Terminal Indicator (TI)
TI_values = []

# Streamlit sidebar inputs
st.sidebar.image("indexcoop.png")
st.sidebar.write("")

current_eth_price_input = st.sidebar.text_input("Current ETH Price ($)", value="1500")
current_eth_price = float(current_eth_price_input)  # Convert the input string to float

# Dropdown to select the outlook on ETH price
eth_outlook = st.sidebar.selectbox("ETH Price Outlook", ["Optimistic", "Neutral", "Pessimistic"], index=1)

days = st.sidebar.selectbox("Time Range (in days)", [15, 30, 60, 90, 180], index=2)

st.sidebar.write("")
st.sidebar.write("")

st.sidebar.markdown("""          
### Methodology
**cbETI's ETH and Simulated Returns Simulations** are very much based on the theory in IC's [proposal](https://gov.indexcoop.com/t/iip-178-launch-the-index-coop-coindesk-eth-trend-index-cdeti/4630). 

Coindesk Indices' ETI is an index that aims to represent market sentiment and assist in momentum strategizing.
                    
Learn more on The Index Coop [here](https://indexcoop.com/) and on Coindesk Indices' ETI [here](https://downloads.coindesk.com/cd3/CDI/Ether+Trend+Indicator+Brochure.pdf).

Visit the [source code](https://github.com/bmvicente/tokensight/blob/main/cbETI.py).                    
""")



# Loop through each day
for day in range(days):
    # For this example, let's assume the outlook is "Neutral" for each day. 
    # You can change this based on your requirements, or even randomize the outlook choice.
    underlying_value = randomize_underlying_index()

    MA = [1, 2.5, 5, 10, 20, 40]

    # Compute MA_results for the current day using the new underlying_value
    MA_results = []
    for h in MA:
        row = next(row for row in data_df_nf if row[0] == h)
        DF = row[headers_df_nf.index("DF")]
        NF = row[headers_df_nf.index("NF")]
        total = sum([(1 - DF) * (DF**i) * NF * underlying_value for i in range(days-1)])
        MA_results.append(total)

    # Compute differences for the current day
    difference_1_5 = MA_results[0] - MA_results[4]
    difference_2_5_10 = MA_results[1] - MA_results[3]
    difference_5_20 = MA_results[2] - MA_results[4]
    difference_10_40 = MA_results[3] - MA_results[5]

    # Compute the Terminal Indicator (TI) for the current day
    MAP1 = np.sign(difference_1_5)
    MAP2 = np.sign(difference_2_5_10)
    MAP3 = np.sign(difference_5_20)
    MAP4 = np.sign(difference_10_40)
    TI = int((MAP1 + MAP2 + MAP3 + MAP4) / 4)
    TI_values.append(TI)

#############################################

# USDC price simulation 

def randomize_usdc_value():
    return random.uniform(0.980, 1.020)

def simulate_usdc_price(days):
    prices = []
    for _ in range(days):
        prices.append(randomize_usdc_value())
    return prices

usdc_prices = simulate_usdc_price(days)


#ETH price simulation

def randomize_eth_change(eth_outlook):
    if eth_outlook == "Neutral":
        return random.uniform(-7.5, 7.5)
    elif eth_outlook == "Pessimistic":
        return random.uniform(-37.5, -7.5)
    elif eth_outlook == "Optimistic":
        return random.uniform(7.5, 37.5)
    else:
        raise ValueError("Invalid outlook provided.")

def simulate_eth_price(initial_price, eth_outlook, days):
    prices = [initial_price]
    for _ in range(days - 1):  # Adjust this line
        change = randomize_eth_change(eth_outlook)
        next_price = prices[-1] + change
        prices.append(next_price)
    return prices

eth_prices = simulate_eth_price(current_eth_price, eth_outlook, days)


#######################################################################


# %USDC calculation
def compute_usdc_percentage(TI):
    if TI == -1:
        return 1
    elif TI == 1:
        return 0
    else:
        return 0.5

# %ETH calculation
def compute_eth_percentage(TI):
    if TI == -1:
        return 0
    elif TI == 1:
        return 1
    else:
        return 0.5

percent_usdc_list = []
percent_eth_list = []

for day in range(days):
    TI_current = TI_values[day]  # Get the TI value for that day
    
    percent_usdc = compute_usdc_percentage(TI_current)
    percent_usdc_list.append(percent_usdc)
    
    percent_eth = compute_eth_percentage(TI_current)
    percent_eth_list.append(percent_eth)


# Rebalance function

def rebalance(TI_values):
    usdc_values = [compute_usdc_percentage(TI_values[0])]  # Start with the first day's %USDC value
    rebalance_flags = [False]  # Start with "FALSE" for the first day

    for i in range(1, len(TI_values)):
        current_usdc = compute_usdc_percentage(TI_values[i])
        usdc_values.append(current_usdc)
        
        if current_usdc != usdc_values[i-1]:
            rebalance_flags.append(True)
        else:
            rebalance_flags.append(False)

    return rebalance_flags

rebalance_results = rebalance(TI_values)
print(rebalance_results)


############################

def calculate_pre_value(usdc_price, pre_usdc_units, eth_prices, pre_eth_units):
    return usdc_price * pre_usdc_units + eth_prices * pre_eth_units

def calculate_post_value(pre_value_today, percent_usdc_prev, percent_usdc_today):
    print("Type of pre_value_today:", type(pre_value_today))
    print("Value of pre_value_today:", pre_value_today)
    
    print("Type of percent_usdc_prev:", type(percent_usdc_prev))
    print("Value of percent_usdc_prev:", percent_usdc_prev)
    
    print("Type of percent_usdc_today:", type(percent_usdc_today))
    print("Value of percent_usdc_today:", percent_usdc_today)
    
    diff = abs(percent_usdc_prev - percent_usdc_today)
    print("Type of diff:", type(diff))
    print("Value of diff:", diff)
    
    multiplier = diff * 0.001 * (1 - (0.0015 / 365))
    print("Type of multiplier:", type(multiplier))
    print("Value of multiplier:", multiplier)
    
    result = pre_value_today - pre_value_today * multiplier
    return result

def calculate_post_units(rebalance, post_value, percent_usdc, usdc_price, percent_eth, eth_prices, pre_usdc_units, pre_eth_units):
    if rebalance:
        post_usdc_units = post_value * percent_usdc / usdc_price
        post_eth_units = post_value * percent_eth / eth_prices
    else:
        post_usdc_units = pre_usdc_units
        post_eth_units = pre_eth_units
        
    return post_usdc_units, post_eth_units

def calculate_returns(post_value, post_value_first_day, eth_prices, eth_price_first_day):
    simulated_return = post_value / post_value_first_day - 1
    eth_return = eth_prices / eth_price_first_day - 1
    
    return simulated_return, eth_return


# Starting values
usdc_price = 1  # Assuming USDC is a stablecoin and its value is 1
eth_price_first_day = current_eth_price
pre_usdc_units = 100
pre_eth_units = 0

# Lists to store results
pre_values = []
post_values = []
pre_usdc_units_list = []
pre_eth_units_list = []
post_usdc_units_list = []
post_eth_units_list = []
simulated_returns = []
eth_returns = []

# Loop over the selected number of days
for day in range(days):
    # Calculate pre_value
    eth_price_today = eth_prices[day]  # This is the current day's ETH price
    pre_value_today = calculate_pre_value(usdc_price, pre_usdc_units, eth_price_today, pre_eth_units)
    pre_values.append(pre_value_today)
    
    pre_usdc_units_list.append(pre_usdc_units)
    pre_eth_units_list.append(pre_eth_units)


    # Determine if rebalancing is needed
    rebalance_flag = rebalance_results[day]
    
    # Calculate post_value
    if day == 0:
        percent_usdc_prev = compute_usdc_percentage(TI_values[day])  # For the first day
    else:
        percent_usdc_prev = compute_usdc_percentage(TI_values[day - 1])
    
    percent_usdc_today = compute_usdc_percentage(TI_values[day])
    post_value_today = calculate_post_value(pre_value_today, percent_usdc_prev, percent_usdc_today)
    post_values.append(post_value_today)
    
    # Calculate post_usdc_units and post_eth_units
    post_usdc, post_eth = calculate_post_units(rebalance_flag, post_value_today, percent_usdc_today, usdc_price, 1 - percent_usdc_today, eth_price_today, pre_usdc_units, pre_eth_units)
    post_usdc_units_list.append(post_usdc)
    post_eth_units_list.append(post_eth)

    # Calculate Simulated return and ETH return
    sim_return, eth_ret = calculate_returns(post_value_today, post_values[0], eth_prices[day], eth_price_first_day)
    simulated_returns.append(sim_return)
    eth_returns.append(eth_ret)

    # For the next day, set pre_usdc_units and pre_eth_units to the current day's post values
    pre_usdc_units = post_usdc
    pre_eth_units = post_eth


#def get_response_from_gpt(data_string, question):
#    messages = [
#        {"role": "system", "content": "You are an analyst. Provide insights based on the given data and the provided methodology. Do not start your response with 'Based on the provided data and methodology' or similar phrasings. Ensure all sentences are complete and end with periods."},
#        {"role": "user", "content": f"{data_string}. {question} Please be concise and limit your answer to about four sentences."}
#    ]
#    
#    response = openai.ChatCompletion.create(
#        model="gpt-3.5-turbo",
#        messages=messages,
#        temperature=0.01,
#        max_tokens=150
#    return response.choices[0].message['content'].strip()


print("Length of TI_values:", len(TI_values))
print("Length of usdc_prices:", len(usdc_prices))
print("Length of eth_prices:", len(eth_prices))
print("Length of percent_usdc_list:", len(percent_usdc_list))
print("Length of percent_eth_list:", len(percent_eth_list))
print("Length of rebalance_results:", len(rebalance_results))
print("Length of pre_values:", len(pre_values))
print("Length of post_values:", len(post_values))
print("Length of post_usdc_units_list:", len(post_usdc_units_list))
print("Length of post_eth_units_list:", len(post_eth_units_list))
print("Length of simulated_returns:", len(simulated_returns))
print("Length of eth_returns:", len(eth_returns))
print("Length of pre_usdc_units_list:", len(pre_usdc_units_list))
print("Length of pre_eth_units_list:", len(pre_eth_units_list))



# Create a dataframe
df = pd.DataFrame({
    'Days': ["Day " + str(i + 1) for i in range(days)],
    'ETI': TI_values,
    'USDC Price': [f"${value:.2f}" for value in usdc_prices],
    'ETH Price': [f"${value:.2f}" for value in eth_prices],
    '% USDC': [f"{value * 100}%" for value in percent_usdc_list],  # Convert to percentage
    '% ETH': [f"{value * 100}%" for value in percent_eth_list],  # Convert to percentage
    'Pre USDC Units': pre_usdc_units_list,
    'Pre ETH Units': pre_eth_units_list,
    'Rebalance': rebalance_results,
    'Pre Value': [f"${value:.2f}" for value in pre_values],  # Prefix with '$' and format to 2 decimal places
    'Post Value': [f"${value:.2f}" for value in post_values],  # Prefix with '$' and format to 2 decimal places
    'Post USDC Units': post_usdc_units_list,
    'Post ETH Units': post_eth_units_list,
    'Simulated Return': [f"{value * 100:.2f}%" for value in simulated_returns],
    'ETH Return': [f"{value * 100:.2f}%" for value in eth_returns]
})


#print(df)

# Create a writer object
#writer = pd.ExcelWriter('cbETI.xlsx', engine='openpyxl')

# Write the dataframe to the Excel file
#df.to_excel(writer, index=False, sheet_name='Sheet1')

#Save the Excel file
#writer.save()

# Create a line chart
fig = go.Figure()

# Add traces for simulated returns and eth returns
fig.add_trace(go.Scatter(x=list(range(1, days+1)), y=simulated_returns,
                         mode='lines', name='Simulated Returns'))
fig.add_trace(go.Scatter(x=list(range(1, days+1)), y=eth_returns,
                         mode='lines', name='ETH Returns'))

# Add titles and labels
fig.update_layout(xaxis_title="Days",
                  yaxis_title="Returns (%)")

# Streamlit User Interface
st.title("The Index Coop: cbETI Simulated Return vs ETH Return")


st.plotly_chart(fig)

## Convert our dataframe to a string
#data_string = f"Outlook: {eth_outlook}. Time Range: {days} days. Methodology: cbETI is derived from randomly selected values from predefined ranges for Leveraged_cbETH and Pendle_stETH_Boosted_APY, dependent on the outlook. The initial APY multiplies this with a constant liquidity providing rate. Subsequent days add a random daily rate to the previous APY. cbETH starts at 3.3% APY, with a compounded yield added each day. Data: {df.to_string(index=False)}"

# Ask the user for a question
#user_question = f"Given the {eth_outlook} outlook over a span of {days} days, provide insights on the progression of the APYs values."

# Get the answer from GPT and display it
#answer = get_response_from_gpt(data_string, user_question)
#st.write(answer)

st.write(df)