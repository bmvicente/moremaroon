import pandas as pd
import requests
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import openpyxl
from io import BytesIO

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
workbook1 = 'XXX'

# Read the xlsx files from GitHub and store headers and data in variables
headers_moving_average_pairs, data_moving_average_pairs = read_xlsx_from_github(workbook1)

print("Headers from Moving Average Pairs.xlsx:")
print(headers_moving_average_pairs)

print("\nHeaders from DF & NF.xlsx:")
print(headers_df_nf)
print("\nData from DF & NF.xlsx:")
print(data_df_nf)

##########################################################

# Convert 'DATE' to datetime and set as index
data['DATE'] = pd.to_datetime(data['DATE'])
data.set_index('DATE', inplace=True)

# Using a Rolling Mean for Prediction
window_size = 7  # 7-day rolling window

# Calculate the rolling mean
rolling_mean = data['APY'].rolling(window=window_size).mean()

# The prediction for the next 30 days will be the mean of the last window_size days
predicted_apy = rolling_mean.iloc[-1]  # Last calculated rolling mean
future_dates = pd.date_range(start=data.index[-1], periods=31, closed='right')  # Generate future dates
future_predictions = pd.Series([predicted_apy] * 30, index=future_dates)  # Repeat this value for the next 30 days

# Create a DataFrame to hold the predicted values
predicted_df = pd.DataFrame(data=future_predictions, columns=['Predicted_APY'])

# Create an interactive plot
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add APY trend line
fig.add_trace(go.Scatter(x=data.index, y=data['APY'], name='Original APY', mode='lines', line=dict(color='blue')), secondary_y=False)

# Add Predicted APY line
fig.add_trace(go.Scatter(x=predicted_df.index, y=predicted_df['Predicted_APY'], name='Predicted APY', mode='lines', line=dict(color='red', dash='dash')), secondary_y=False)

# Update plot layout
fig.update_layout(title='APY Trend and Prediction', xaxis_title='Date', yaxis_title='APY (%)', legend_title='Legend', hovermode='x')

# Show plot
fig.show()

# Display the DataFrame with predicted APY values
predicted_df
