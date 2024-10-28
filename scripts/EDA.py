# Librerias
import pandas as pd
from IPython.display import display
import folium
from folium.plugins import HeatMap
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno

# Cargue de los datos
url = '../data/RTOP.csv'
df = pd.read_csv(url, encoding='ISO-8859-1')

df=df.rename(columns={'Ship ID - Ship Classification':'Vessel Type','Ship - Name':'Ship Name'})

print(df)
