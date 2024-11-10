import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import datetime as dt

# Inicializar la aplicación
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Dashboard de Arribos de Barcos"

server = app.server
app.config.suppress_callback_exceptions = True

# Cargar datos simulados (esto debes reemplazarlo con tu dataset real)
def load_data():
    np.random.seed(42)
    date_rng = pd.date_range(start='2024-01-01', end='2024-12-31', freq='H')
    data = pd.DataFrame(date_rng, columns=['timestamp'])
    data['Barco'] = np.random.choice(['Barco A', 'Barco B', 'Barco C'], size=(len(data)))
    data['Origen'] = np.random.choice(['Puerto 1', 'Puerto 2', 'Puerto 3'], size=(len(data)))
    data['Arribo_real'] = np.random.randint(0, 100, size=(len(data)))
    data['Proyeccion_arribo'] = data['Arribo_real'] + np.random.randint(-10, 10, size=(len(data)))
    
    # Límites de predicción
    data['Upper_bound'] = data['Proyeccion_arribo'] + 10
    data['Lower_bound'] = data['Proyeccion_arribo'] - 10
    
    return data

# Cargar datos
data = load_data()

# Graficar serie de arribos
def plot_series(data, initial_date, proy):
    data_plot = data.loc[data['timestamp'] >= initial_date]
    data_plot = data_plot[:proy]
    
    fig = go.Figure([
        go.Scatter(
            name='Arribos Reales',
            x=data_plot['timestamp'],
            y=data_plot['Arribo_real'],
            mode='lines',
            line=dict(color="#188463"),
        ),
        go.Scatter(
            name='Proyección',
            x=data_plot['timestamp'],
            y=data_plot['Proyeccion_arribo'],
            mode='lines',
            line=dict(color="#bbffeb"),
        ),
        go.Scatter(
            name='Upper Bound',
            x=data_plot['timestamp'],
            y=data_plot['Upper_bound'],
            mode='lines',
            line=dict(width=0),
            showlegend=False
        ),
        go.Scatter(
            name='Lower Bound',
            x=data_plot['timestamp'],
            y=data_plot['Lower_bound'],
            fill='tonexty',
            fillcolor="rgba(242, 255, 251, 0.3)",
            line=dict(width=0),
            mode='lines',
            showlegend=False
        )
    ])

    fig.update_layout(
        yaxis_title='Cantidad de Barcos',
        hovermode="x",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="#2cfec1",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_xaxes(showgrid=True, gridcolor='#7C7C7C')
    fig.update_yaxes(showgrid=True, gridcolor='#7C7C7C')

    return fig

# Panel de control
def generate_control_card():
    return html.Div(
        id="control-card",
        children=[
            html.P("Seleccionar fecha y hora inicial:"),
            dcc.DatePickerSingle(
                id='datepicker-inicial',
                min_date_allowed=min(data['timestamp'].dt.date),
                max_date_allowed=max(data['timestamp'].dt.date),
                initial_visible_month=min(data['timestamp'].dt.date),
                date=max(data['timestamp'].dt.date)-dt.timedelta(days=7)
            ),
            html.Br(),
            html.P("Seleccionar hora inicial:"),
            dcc.Dropdown(
                id="dropdown-hora-inicial",
                options=[{"label": str(i).zfill(2), "value": i} for i in range(24)],
                value=pd.to_datetime(max(data['timestamp'])-dt.timedelta(days=7)).hour,
            ),
            html.Br(),
            html.P("Ingresar horas a proyectar:"),
            dcc.Slider(
                id="slider-proyeccion",
                min=1,
                max=120,
                step=1,
                value=24,
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True},
            )
        ]
    )

# Layout de la aplicación
app.layout = html.Div(
    id="app-container",
    children=[
        html.Div(
            id="left-column",
            className="four columns",
            children=[generate_control_card()]
        ),
        html.Div(
            id="right-column",
            className="eight columns",
            children=[
                html.Div(
                    id="model_graph",
                    children=[
                        html.B("Proyección de Arribos de Barcos"),
                        dcc.Graph(id="plot_series")
                    ],
                )
            ],
        ),
    ],
)

# Callback para actualizar la gráfica
@app.callback(
    Output("plot_series", "figure"),
    [Input("datepicker-inicial", "date"),
     Input("dropdown-hora-inicial", "value"),
     Input("slider-proyeccion", "value")]
)
def update_plot(date, hour, proy):
    if date and hour is not None:
        initial_date = f"{date} {str(hour).zfill(2)}:00:00"
        initial_date = pd.to_datetime(initial_date, format="%Y-%m-%d %H:%M:%S")

        # Generar la gráfica
        fig = plot_series(data, initial_date, proy)
        return fig

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True)
