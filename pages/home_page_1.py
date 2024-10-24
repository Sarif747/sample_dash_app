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
        "Clarke County", "Oconee County", "Madison County", "Jackson County",
        "Morgan County", "Barrow County", "Walton County", "Greene County",
        "Newton County", "Jasper County", "Hall County", "Habersham County"
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
training_types = df['Training Type'].unique()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

fig_map = px.scatter_mapbox(
    df,
    lat='Latitude',
    lon='Longitude',
    size='Participants',
    color='Training Type',
    hover_name='Counties Served',
    hover_data=['Participants', 'Training Type'],
    mapbox_style="carto-positron",
    zoom=6,
    center={"lat": 33.9519, "lon": -83.5541},
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

fig_scatter.update_layout(
    title='Participants by Date, County, and Training Type',
    title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    hovermode='closest'
)

fig_scatter.update_xaxes(
    title_text='Date',
    title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    tickformat='%Y'
)

fig_scatter.update_yaxes(
    title_text='Total Participants',
    title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold')
)

def home_1_plot():
    return html.Div([
    html.H2("Training Overview", style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
    dbc.Row([
        dbc.Col(
            html.Div(
                style={
                    'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                    'borderRadius': '10px',
                    'padding': '10px',
                    'backgroundColor': 'white',
                    'margin': '20px auto',
                    'width': '90%',
                },
                children=[
                    dcc.Graph(
                        id='map-graph',
                        figure=fig_map,
                        style={'width': '100%', 'height': '600px', 'margin': 'auto'}
                    ),
                ]
            ),width=8),
        dbc.Col(
            html.Div([
                
                    html.H2('COALITION TRAININGS',style={'textAlign': 'left', 'marginLeft': '0px', 'color': 'darkgreen'}),
                    html.P("In 2022, Resilient Northeast Georgia has honed its training approach to be more county-specific by"
                            "splitting the region into clusters determined by geographic proximity, thematic similarity of"
                            "strategic plans, areas of interest for collaborative expansion, and the leadership and insights of the"
                            "regional manager. As a result, the collaborative focused energy on smaller, more specialized"
                            "training modalities than years past, prioritizing depth of impact and usability of skills acquired in"
                            "the training in an effort to improve sustainability of retained regional knowledge over time."),
                        html.Strong("Note**\n"),
                        html.P(
                        "CRMI - Community Resiliency Model Introduction\n"
                        "YMHAW - Youth Mental Health First Aid Workshop\n"
                        "CRMW - Community Resiliency Model Workshop\n"
                        "CMW - Connections Matter Workshop\n"
                        "ACE/CRM - The Business Case for ACE's/CRM Intro Hybrid\n"
                        "CSFT - Circle of Security Facilitator Training",
                        style={'whiteSpace': 'pre-line'}
                    ),
                    html.P("Select the Training Type"),
                    dcc.Dropdown(
                        id='training-type-dropdown',
                        options=[{'label': training_type, 'value': training_type} for training_type in training_types],
                        value=training_types[0],
                        clearable=False,
                        style={
                            'width': '200px',
                            'height': '40px',
                            'marginLeft': '25px',
                            'textAlign': 'center',
                            'color': 'darkgreen'
                        },
                    )
                ],
            ),style={
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center',
            'height': '50%'  
        }
    )
    ]),
    dbc.Row(),
    dbc.Row([
        dbc.Col(
            html.Div(
                
                dcc.Graph(
                    id='scatter-graph',
                    figure=fig_scatter,
                    style={'width': '100%', 'height': '500px', 'margin': 'auto'}
                )
            ),style={
                    'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                    'borderRadius': '10px',
                    'padding': '10px',
                    'backgroundColor': 'white',
                    'margin': '20px auto',
                    'width': '80%',
                },
        )
    ]),
], style={'backgroundColor': 'lightgreen', 'padding': '20px'})


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
        mapbox_style="carto-positron",
        zoom=6,
        center={"lat": 33.9519, "lon": -83.5541},
        title=f'Participants Distribution in Georgia for {selected_training_type}',
    )

    fig_map.update_layout(
        title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
        hovermode='closest'
    )

    return fig_map

if __name__ == '__main__':
    app.run_server(debug=True)
