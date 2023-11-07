import pandas as pd

def calculate_apy(starting_apy, r_annual, timeframe_days, n):
    r_period = r_annual / (365 / timeframe_days)
    days_per_period = timeframe_days / n
    timeframes = [0] + [int(days_per_period * period) for period in range(1, n + 1)]

    df = pd.DataFrame({'Time Range (Days)': timeframes, 'APY': [starting_apy * 100] + [None] * n})

    for period in range(1, n + 1):
        APY = ((1 + r_period)**period - 1 + starting_apy) * 100
        df.loc[period, 'APY'] = APY

    df['APY'] = df['APY'].apply(lambda x: f'{x:.2f}%')
    return df
