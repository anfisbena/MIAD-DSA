import dash
from dash import html, dcc
import folium
from folium.plugins import HeatMap
from scripts.countryCoordinates import country_coordinates as coords

def initialize_app():
    app = dash.Dash(
        __name__,
        meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
        assets_folder='../assets/'
    )
    app.title = "Dashboard de Arribos de Barcos"
    app.config.suppress_callback_exceptions = True
    return app

def generate_control_card(data):
    ship_list=data['Ship Name'].sort_values().unique()
    return html.Div(
        id="control-card",
        children=[
            html.P("Seleccionar un barco:"),
            dcc.Dropdown(
                id="dropdown-Ship-Name",
                options=ship_list
            ),
            html.Br(),
        ]
    )

def plot_heatmap(data,ShipName=None, country_coordinates=coords):
    if ShipName!=None:
        data=data[data['Ship Name']==ShipName] 
    country = data['Country'].value_counts()

    # Crear el mapa base centrado en el mundo
    world_map = folium.Map(location=[20, 0], zoom_start=2)

    # Crear una lista para almacenar las coordenadas y las frecuencias (para el HeatMap)
    heat_data = []

    # Recorrer las filas de la frecuencia de países y agregar los puntos con la frecuencia (intensidad)
    for country, count in country.items():
        if country in country_coordinates:
            # Agregar la coordenada y la frecuencia (count) como intensidad
            heat_data.append([country_coordinates[country][0], country_coordinates[country][1], count])

    # Crear el HeatMap y agregarlo al mapa
    HeatMap(heat_data).add_to(world_map)

    # Retornar el mapa en formato HTML
    return world_map._repr_html_()
