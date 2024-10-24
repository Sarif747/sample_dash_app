import pandas as pd
import random
from datetime import datetime, timedelta
import plotly.express as px
import dash
from dash import dcc, html
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

fig_map = px.scatter_mapbox(
    df,
    lat='Latitude',
    lon='Longitude',
    size='Participants',
    color='Training Type',
    hover_name='Counties Served',
    hover_data=['Participants'],
    mapbox_style="carto-positron",
    zoom=6,
    center={"lat": 32.1656, "lon": -82.9001},
    title='Participants Distribution in Georgia by County and Training Type',
)

fig_scatter = px.scatter(
    df,
    x='Date',
    y='Participants',
    color='Training Type',
    hover_name='Counties Served',
    title='Participants by Date, County, and Training Type',
    labels={'Participants': 'Total Participants'},
)

fig_scatter.update_layout(title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'))
fig_scatter.update_xaxes(title_text='Date', tickformat='%Y-%m-%d')
fig_scatter.update_yaxes(title_text='Total Participants')

app.layout = html.Div([
    html.H2("Training Overview", style={'textAlign': 'left', 'color': 'darkgreen'}),
    dcc.Graph(
        id='map-graph',
        figure=fig_map,
        style={'width': '100%', 'height': '600px'}
    ),
    dcc.Graph(
        id='scatter-graph',
        figure=fig_scatter,
        style={'width': '100%', 'height': '400px'}
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

if __name__ == '__main__':
    app.run_server(debug=True)
