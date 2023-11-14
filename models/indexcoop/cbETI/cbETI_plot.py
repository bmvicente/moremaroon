import plotly.graph_objects as go

def create_plot(days, simulated_returns, eth_returns):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(1, days+1)), y=simulated_returns, mode='lines', name='Simulated Returns'))
    fig.add_trace(go.Scatter(x=list(range(1, days+1)), y=eth_returns, mode='lines', name='ETH Returns'))
    fig.update_layout(xaxis_title="Days", yaxis_title="Returns (%)")
    return fig