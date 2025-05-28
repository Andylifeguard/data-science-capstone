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
    if not {'Launch Site', 'Payload Mass (kg)', 'class', 'Booster Version Category'}.issubset(spacex_df.columns):
        raise KeyError("Faltan columnas esperadas en el dataset")
    max_payload = spacex_df['Payload Mass (kg)'].max()
    min_payload = spacex_df['Payload Mass (kg)'].min()
except FileNotFoundError:
    print("Error: No se encontró el archivo spacex_launch_dash.csv.")
    exit(1)
except KeyError as e:
    print(f"Error: {e}")
    exit(1)

# Crear la aplicación Dash
app = Dash(__name__)

# Crear el layout de la aplicación
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    html.Br(),

    # Dropdown para seleccionar el sitio de lanzamiento
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] + 
                [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
        value='ALL',
        placeholder="Selecciona un sitio de lanzamiento",
        searchable=True
    ),
    html.Br(),

    # Gráfico de pastel para mostrar éxito/fallo
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    # Slider para rango de carga útil
    html.P("Rango de carga útil (kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=int(max_payload) + 1000,  # Ajustar al máximo del dataset
        step=1000,
        marks={i: str(i) for i in range(0, int(max_payload) + 1000, 2500)},
        value=[min_payload, max_payload]
    ),

    # Gráfico de dispersión para correlación carga útil-éxito
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Callback para el gráfico de pastel
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(
            spacex_df,
            values='class',
            names='Launch Site',
            title='Lanzamientos exitosos por sitio',
            color_discrete_map={0: 'red', 1: 'green'}
        )
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        success_counts = filtered_df['class'].value_counts().reset_index()
        success_counts.columns = ['class', 'count']
        success_counts['Outcome'] = success_counts['class'].map({1: 'Éxito', 0: 'Fallo'})
        fig = px.pie(
            success_counts,
            values='count',
            names='Outcome',
            title=f'Resultados de lanzamientos para {entered_site}',
            color='Outcome',
            color_discrete_map={'Éxito': 'green', 'Fallo': 'red'}
        )
    return fig

# Callback para el gráfico de dispersión
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def get_scatter_plot(entered_site, payload_range):
    min_payload, max_payload = payload_range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= min_payload) &
        (spacex_df['Payload Mass (kg)'] <= max_payload)
    ]
    if entered_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
    
    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Correlación entre carga útil y éxito' if entered_site == 'ALL' else f'Correlación para {entered_site}',
        labels={'class': 'Resultado (1=Éxito, 0=Fallo)'},
        hover_data=['Launch Site']
    )
    return fig

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
