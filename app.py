from scripts.dashboard import initialize_app, generate_control_card, plot_heatmap
from scripts.ETL import load_data
from scripts.modelo import rand_class
from dash import html
from dash.dependencies import Input, Output


# Inicializar la aplicación
app = initialize_app()
server = app.server

# Cargar datos
datasource='data/RTOP.csv'
data=load_data(datasource)
# Uso de la función con el dataset df_clean
location_accuracy,location_mse,location_r2,predicted_location=rand_class(data)

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
                html.H4(id='predicted-location',style={'color':'Red'}),
                ], 
            style={'width': '100%', 'textAlign': 'center', 'padding': '20px'} 
        ),
        html.Div(
            id="left-column",
            className="four columns",
            children=[
                html.H4("Estadisticas del modelo"),
                html.P(id="location-accuracy"),
                html.P(id="location-mse"),
                html.P(id="location-r2"),
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
@app.callback([
        Output("folium-map", "srcDoc"),
        Output("predicted-location", "children"),
        Output("location-accuracy", "children"),
        Output("location-mse", "children"),
        Output("location-r2", "children")
    ],
    [
        Input("dropdown-Ship-Name", "value")
    ]
)


def update_plot(ShipName):
    if not ShipName: 
        return "", "", "", "", ""
    map_html = plot_heatmap(data,ShipName)
    predicted_location,location_accuracy,location_mse,location_r2  = rand_class(data, ShipName) 
    accuracy_text = f"Precisión de Ubicación (Clasificación): {location_accuracy * 100:.2f}%" 
    mse_text = f"Error Cuadrático Medio de Ubicación: {location_mse:.2f}" 
    r2_text = f"R^2 de Ubicación: {location_r2:.2f}"
    return map_html, predicted_location,accuracy_text, mse_text, r2_text

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True)
