import plotly.graph_objects as go

def create_plot(icDEY_APYs, cbETH_APYs, time_range):
    """Create and return a Plotly graph object for the APY data."""
    fig = go.Figure()

    # Add icDEY APY trace
    fig.add_trace(go.Scatter(
        x=list(range(1, time_range+1)),
        y=icDEY_APYs,
        mode='lines',
        name='icDEY APY',
        line=dict(color="Black")
    ))

    # Add cbETH APY trace
    fig.add_trace(go.Scatter(
        x=list(range(1, time_range+1)),
        y=cbETH_APYs,
        mode='lines',
        name='cbETH APY',
        line=dict(color="Blue")
    ))

    # Update layout
    fig.update_layout(
        xaxis_title='Days',
        yaxis_title='APY',
        hovermode='x unified',
        yaxis=dict(range=[0, 17], tickvals=list(range(0, 18, 5)), ticktext=[f"{i}%" for i in range(0, 18, 5)])
    )

    return fig