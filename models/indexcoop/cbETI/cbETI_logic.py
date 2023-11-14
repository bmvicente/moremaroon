import random
import numpy as np

def randomize_underlying_index():
    return random.uniform(-20, 20)

def randomize_usdc_value():
    return random.uniform(0.980, 1.020)

def randomize_eth_change(eth_outlook):
    if eth_outlook == "Neutral":
        return random.uniform(-7.5, 7.5)
    elif eth_outlook == "Pessimistic":
        return random.uniform(-37.5, -7.5)
    elif eth_outlook == "Optimistic":
        return random.uniform(7.5, 37.5)
    else:
        raise ValueError("Invalid outlook provided.")

def compute_usdc_percentage(TI):
    return { -1: 1, 1: 0, 0: 0.5 }[TI]

def compute_eth_percentage(TI):
    return { -1: 0, 1: 1, 0: 0.5 }[TI]

def rebalance(TI_values):
    usdc_values, rebalance_flags = [compute_usdc_percentage(TI_values[0])], [False]
    for i in range(1, len(TI_values)):
        current_usdc = compute_usdc_percentage(TI_values[i])
        usdc_values.append(current_usdc)
        rebalance_flags.append(current_usdc != usdc_values[i-1])
    return rebalance_flags

def calculate_pre_value(usdc_price, pre_usdc_units, eth_prices, pre_eth_units):
    return usdc_price * pre_usdc_units + eth_prices * pre_eth_units

def calculate_post_value(pre_value_today, percent_usdc_prev, percent_usdc_today):
    diff = abs(percent_usdc_prev - percent_usdc_today)
    multiplier = diff * 0.001 * (1 - (0.0015 / 365))
    return pre_value_today - pre_value_today * multiplier

def calculate_post_units(rebalance, post_value, percent_usdc, usdc_price, percent_eth, eth_prices, pre_usdc_units, pre_eth_units):
    return (post_value * percent_usdc / usdc_price, post_value * percent_eth / eth_prices) if rebalance else (pre_usdc_units, pre_eth_units)

def calculate_returns(post_value, post_value_first_day, eth_prices, eth_price_first_day):
    return (post_value / post_value_first_day - 1, eth_prices / eth_price_first_day - 1)
