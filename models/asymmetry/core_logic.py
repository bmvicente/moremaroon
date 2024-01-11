import random
import streamlit as st

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

    # Think of always positive compounding, just in different scales.
    # Option in simulation to select compounding or not
    # Check DefiLlama Base APY info

    Daily_Rate = [(-0.0075, 0.001),(-0.005,0.005),(-0.001, 0.0075)]

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
        APY_next = APYs[-1] * (1 + daily_rate) 
        APYs.append(APY_next)

    return APYs


    
def compute_seven_day_avg(apy_values):
    averages = []
    for idx, value in enumerate(apy_values):
        if idx < 6:  # For the first 6 days, average with all previous values including the current one
            averages.append(sum(apy_values[:idx+1]) / (idx+1))
        else:  # From the 7th day onward, compute the 7-day rolling average
            averages.append(sum(apy_values[idx-6:idx+1]) / 7)
    return averages


