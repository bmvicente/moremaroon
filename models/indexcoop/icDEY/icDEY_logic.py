import random
import pandas as pd


def get_random_value(interval, idx):
    """Generates a random value from an interval based on the given outlook index."""
    lower, upper = interval[idx]
    return random.uniform(lower, upper)

def APY_to_DPY(apy):
    """Converts APY to DPY."""
    return (1 + apy) ** (1/365) - 1

def simulate_icDEY_APY(outlook, time_range):
    """Simulate icDEY APY based on the given outlook and time range."""
    # Given outlook, get index
    outlook_map = {"Optimistic": 2, "Neutral": 1, "Pessimistic": 0}
    outlook_idx = outlook_map[outlook]

    Leveraged_cbETH = [(3.8, 4.7), (4.8, 5.7), (5.8, 6.7)]
    Liquidity_Providing = 0.3
    wstETH = [(1.5, 3), (3, 4), (4, 5.5)]
    Daily_Rate = [(0.0025, 0.0125), (0.0126, 0.020), (0.021, 0.040)]

    # Only first APY is random
    first_APY = ((get_random_value(Leveraged_cbETH, outlook_idx) * (1 + Liquidity_Providing)) * (1 + get_random_value(wstETH, outlook_idx)))
    APYs = [first_APY]

    for _ in range(1, time_range):
        daily_rate = get_random_value(Daily_Rate, outlook_idx)
        APYs.append(APYs[-1] + daily_rate)

    return APYs

def simulate_cbETH_APY(time_range):
    """Simulate cbETH APY for a given time range."""
    cbETH_APY = 3.3
    APYs_cbETH = [cbETH_APY]
    for i in range(1, time_range):
        cbETH_APY += APY_to_DPY(cbETH_APY)
        APYs_cbETH.append(cbETH_APY)
    return APYs_cbETH

