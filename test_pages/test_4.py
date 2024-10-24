import pandas as pd
import random
from datetime import datetime, timedelta
import plotly.express as px
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

def generate_synthetic_data(start_year, end_year, num_entries):
    synthetic_data = {
        "Date": [],
        "Counties Served": [],
        "Participants": [],
        "Training Type": []
    }
    counties = [
        "Clarke County",
        "Oconee County",
        "Madison County",
        "Jackson County",
        "Morgan County",
        "Barrow County",
        "Walton County",
        "Greene County",
        "Newton County",
        "Jasper County",
        "Hall County",
        "Habersham County"
    ]
    training_types = ["CRMI", "YMHAW", "CRMW", "CMW", "ACE/CRM", "CSFT"]

    for _ in range(num_entries):
        random_days = random.randint(0, (datetime(end_year, 12, 31) - datetime(start_year, 1, 1)).days)
        random_date = (datetime(start_year, 1, 1) + timedelta(days=random_days)).strftime("%Y-%m-%d")

        synthetic_data["Date"].append(random_date)
        synthetic_data["Counties Served"].append(random.choice(counties))
        synthetic_data["Participants"].append(random.randint(5, 50))
        synthetic_data["Training Type"].append(random.choice(training_types))

    return synthetic_data

synthetic_data = generate_synthetic_data(2019, 2024, 100)
df = pd.DataFrame(synthetic_data)

df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year

county_coordinates = {
    "Clarke County": (33.9519, -83.3576),
    "Oconee County": (33.8679, -83.4372),
    "Madison County": (34.0993, -83.2195),
    "Jackson County": (34.1176, -83.5495),
    "Morgan County": (33.6174, -83.5962),
    "Barrow County": (34.0143, -83.6887),
    "Walton County": (33.7705, -83.7209),
    "Greene County": (33.5707, -83.1292),
    "Newton County": (33.5540, -83.8610),
    "Jasper County": (33.0018, -83.7350),
    "Hall County": (34.3036, -83.7650),
    "Habersham County": (34.5990, -83.5541)
}

df['Latitude'] = df['Counties Served'].apply(lambda x: county_coordinates.get(x, (0, 0))[0])
df['Longitude'] = df['Counties Served'].apply(lambda x: county_coordinates.get(x, (0, 0))[1])

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

training_types = df['Training Type'].unique()

app.layout = html.Div([
    html.H2("Training Overview", style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
    dcc.Dropdown(
        id='training-type-dropdown',
        options=[{'label': training_type, 'value': training_type} for training_type in training_types],
        value=training_types[0],  
        clearable=False,
        style={'width': '100%', 'height': '400px', 'margin': 'auto'}
    ),
    dcc.Graph(
        id='map-graph',
        style={'width': '100%', 'height': '400px', 'margin': 'auto'}
    ),
    dbc.Row([
        dbc.Col(
            html.Div(
                [
                    html.H2('COALITION TRAININGS', style={'textAlign': 'left', 'color': 'darkgreen'}),
                    html.P("In 2022, Resilient Northeast Georgia has honed its training approach..."),
                    html.Strong("Note**\n"),
                    html.P(
                        "CRMI - Community Resiliency Model Introduction\n"
                        "YMHAW - Youth Mental Health First Aid Workshop\n"
                        "CRMW - Community Resiliency Model Workshop\n"
                        "CMW - Connections Matter Workshop\n"
                        "ACE/CRM - The Business Case for ACE's/CRM Intro Hybrid\n"
                        "CSFT - Circle of Security Facilitator Training",
                        style={'whiteSpace': 'pre-line'}
                    )
                ]
            )
        )
    ])
], style={'backgroundColor': 'lightgreen', 'padding': '20px'})

@app.callback(
    Output('map-graph', 'figure'),
    Input('training-type-dropdown', 'value')
)

def update_map(selected_training_type):
    filtered_df = df[df['Training Type'] == selected_training_type]

    fig_map = px.scatter_mapbox(
        filtered_df,
        lat='Latitude',
        lon='Longitude',
        size='Participants',
        color='Training Type',
        hover_name='Counties Served',
        hover_data=['Participants'],
        mapbox_style="carto-darkmatter",
        zoom=6,
        center={"lat": 33.9519, "lon": -83.5541},
        title=f'Participants Distribution in Georgia for {selected_training_type}',
    )

    return fig_map

if __name__ == '__main__':
    app.run_server(debug=True)