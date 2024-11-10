from scripts.dashboard import initialize_app, generate_control_card, plot_heatmap
from scripts.ETL import load_data
from dash import html
from dash.dependencies import Input, Output

# Inicializar la aplicación
app = initialize_app()
server = app.server

# Cargar datos
datasource='data/RTOP.csv'
data=load_data(datasource)
# Uso de la función con el dataset df_clean


# Layout de la aplicación
app.layout = html.Div(
    id="app-container",
    children=[
        html.Div( 
            id="header", 
            children=[ 
                html.H1("Dashboard de predicción de barcos"), 
                html.P("A continuación, puede seleccionar el barco en el siguiente menú desplegable para predecir el posible proximo puerto al que este va a llegar."),
                html.Div(generate_control_card(data), style={ 'width': '30%','margin':'auto'}),
                html.Br(),
                html.P("El modelo predice que el proximo puerto es:"),
                html.H4('PONCE',style={'color':'Red'}),
                ], 
            style={'width': '100%', 'textAlign': 'center', 'padding': '20px'} 
        ),
        html.Div(
            id="left-column",
            className="four columns",
            children=[
                html.H4("Estadisticas del modelo"),
                html.P("Precision de Ubicación: 75.00%"),
                html.P("Error Cuadrático Medio de Ubicación: 0.25"),
                html.P('R^2 de Ubicación: 0.95'),
            ]
        ),
        html.Div(
            id="right-column",
            className="eight columns",
            children=[
                html.Div(
                    id="model_map",
                    children=[
                        html.H4("Mapa de Calor de Arribos",style={'margin':'auto','text-align':'center'}),
                        html.Iframe(id="folium-map", srcDoc=plot_heatmap(data), width="100%", height="600")
                    ],
                )
            ],
        ),
    ],
)

# Callback para actualizar la gráfica
@app.callback(
    Output("folium-map", "srcDoc"),
    [Input("dropdown-Ship-Name", "value")
    ]
)


def update_plot(ShipName):
    map_html = plot_heatmap(data,ShipName)
    return map_html

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True)
