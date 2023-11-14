import random
import streamlit as st
import openai

def get_random_value(interval):
    """Generates a random value from an interval."""
    lower, upper = interval
    return random.uniform(lower, upper)

def calculate_var_stETH_APY(outlook, CP, CstETH, CV):
    outlook_map = {
        "Optimistic": 0,
        "Neutral": 1,
        "Pessimistic": 2,
        "Predict For Me (Coming Soon)": None
    }

    FP_ranges = [(1500.00, 1900.00), (1900.00, 2100.00), (2100.00, 2500.00)]
    #[(1300.00, 1550.00), (1550.00, 1750.00), (1750.00, 2000.00)]
    FstETH_ranges = [(1.50, 3.50), (3.50, 5.00), (5.00, 7.00)]
    #[(2.00, 3.25), (3.25, 4.25), (4.25, 5.50)]
    FV_ranges = [(780000, 820000), (820000, 850000), (850000, 890000)]

    outlook_idx = outlook_map[outlook]

    FP = get_random_value(FP_ranges[outlook_idx])
    FstETH = get_random_value(FstETH_ranges[outlook_idx])
    FV = get_random_value(FV_ranges[outlook_idx])

    var_stETH_APY_next = (1/5)*((FP-CP)/CP) * (1/2)*((FstETH-CstETH)/CstETH) * (3/10)*((FV-CV)/CV)
    return var_stETH_APY_next

# Add in Asymmetry simulatiom
def compute_seven_day_avg(apy_values):
    averages = []
    for idx, value in enumerate(apy_values):
        if idx < 6:  # For the first 6 days, average with all previous values including the current one
            averages.append(sum(apy_values[:idx+1]) / (idx+1))
        else:  # From the 7th day onward, compute the 7-day rolling average
            averages.append(sum(apy_values[idx-6:idx+1]) / 7)
    return averages