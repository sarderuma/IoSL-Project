import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
app = dash.Dash()

app.layout = html.Div(
        dcc.Graph(
            id='my-graph',
            figure=dict(
                data=[
                    dict(x=[5, 10, 15, 20, 25, 30, 35, 40], y=[85, 137, 212, 298, 386, 474, 566, 652],
                    name='HTTP REST API',
                    marker=dict(color='rgb(55, 83, 109)')
                    ),
                    dict(x=[5, 10, 15, 20, 25, 30, 35, 40], y=[99, 157, 253, 312, 384, 489, 553, 643],
                    name='Service Mesh-istio',
                    marker=dict(color='rgb(26, 118, 255)')
                    )
                ],
                layout=dict(
                    
                    yaxis=dict(title='Average Communication Overhead (ms)'),
                    xaxis=dict(title='Number of Microservices'),
                    showlegend=True,
                    legend=dict(x=0.5, y=1.0),
                    margin=dict(l=60, r=10, t=70, b=60)
                )
            ),
        style={'height': 300},
    
        ),
)         


if __name__ == '__main__':
    app.run_server(debug=True)        