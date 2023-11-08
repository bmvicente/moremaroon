import plotly.graph_objects as go
import numpy as np

def create_apy_plot(days, APYs_7_day_avg, initial_APY):
    y_axis_min = initial_APY - 2.5  # 2.5% below the starting APY
    y_axis_max = initial_APY + 2.5  # 2.5% above the starting APY

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(1, days+1)), y=APYs_7_day_avg, mode='lines', name='safETH APY'))
    fig.update_layout(
        hovermode='x unified',
        xaxis_title="Days",
        yaxis_title="APY",
        showlegend=True
    )
    fig.update_yaxes(
        range=[y_axis_min, y_axis_max],
        dtick=0.05,
        tickvals=[val for val in np.linspace(y_axis_min, y_axis_max, 10)],
        ticktext=[f"{val:.2f}%" for val in np.linspace(y_axis_min, y_axis_max, 10)]
    )

    return fig
