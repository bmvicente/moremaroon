import plotly.graph_objects as go

def create_apy_plot(df):
    fig = go.Figure(data=go.Scatter(x=df['Time Range (Days)'], y=df['APY'].str.rstrip('%').astype(float), mode='lines+markers', hoverinfo='x+y'))
    fig.update_layout(hovermode='x unified',
                      xaxis_title='Time Range (Days)',
                      yaxis_title='APY (%)',
                      xaxis=dict(
                          tickmode='linear',
                          tick0=0,
                          dtick=15))
    return fig
