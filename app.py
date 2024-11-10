from scripts.dashboard import initialize_app, generate_control_card, plot_region_and_heatmap
from scripts.ETL import load_data
from dash import html, dcc
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
            id="left-column",
            className="four columns",
            children=[generate_control_card(data)]
        ),
        html.Div(
            id="right-column",
            className="eight columns",
            children=[
                html.Div(
                    id="model_map",
                    children=[
                        html.B("Mapa de Calor de Arribos"),
                        html.Iframe(id="folium-map", srcDoc=plot_region_and_heatmap(data, ), width="100%", height="600")
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
    map_html = plot_region_and_heatmap(data,ShipName)
    return map_html

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True)
