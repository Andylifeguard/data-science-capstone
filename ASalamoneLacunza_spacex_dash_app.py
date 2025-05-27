# Andres Salamone Lacunza 2025-05-23
# Gracias a JonathanMClark por la referencia

# Importar librerías necesarias
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Cargar los datos de SpaceX en un DataFrame con manejo de errores
try:
    spacex_df = pd.read_csv("spacex_launch_dash.csv")
    max_payload = spacex_df['Payload Mass (kg)'].max()
    min_payload = spacex_df['Payload Mass (kg)'].min()
except FileNotFoundError:
    print("Error: No se encontró el archivo spacex_launch_dash.csv.")
    exit(1)
except KeyError as e:
    print(f"Error: Falta una columna esperada en el dataset: {e}")
    exit(1)

# Función para asignar resultado de lanzamiento (no usada actualmente, pero mantenida por si se