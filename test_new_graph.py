from sqlalchemy import create_engine, text
import dash
from dash import dcc,html
import plotly.express as px
import pandas as pd
import random
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
import requests
from urllib.request import urlopen
import json

geolocator = Nominatim(user_agent="address_locator")
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
app = dash.Dash(__name__)

def get_db_connection():
    server = 'mydb-rg.database.windows.net'
    database = 'my_db_rg'
    username = 'Sarif747'
    password = 'Sa%408790883008'
    db_connection_str = (
        f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+18+for+SQL+Server"
    )
    try:
        engine = create_engine(db_connection_str)
        print("arif")
        with engine.connect() as conn:
            print("Connection successful")
        return engine
    except Exception as e:
        print(f"Error: {e}")
        return None

conn = get_db_connection()
if conn:
    query = "SELECT * FROM Events"
    df = pd.read_sql(query, conn)
    print(df)


def map_figure():
    conn = get_db_connection()
    if conn:
        query = "SELECT * FROM Events"
        df = pd.read_sql(query, conn)
        print(df)

    fig = px.choropleth_mapbox(
        df, 
        geojson=counties,  # Replace None with your custom GeoJSON or use default mapbox boundaries
        locations="Event_Name",  # You can use 'Event_Name' or other categorical values if needed
        color="Number_Trained",  # Change to "Number_Trained" or any numeric field to visualize
        hover_name="Event_Name", 
        hover_data={
            "County": True, 
            "Number_Trained": True, 
            "Hours": True, 
            "Date": True,
            "Address": True, 
            "Population_Served": True, 
            "Demographic_Information": True, 
            "Identified_Gaps": True, 
            "Latitude": False,  
            "Longitude": False  
        },
        color_continuous_scale="Viridis",  # Use any color scale you prefer
        range_color=(0, 100),  # Adjust range depending on your data (e.g., range of Number_Trained)
        title="Event Locations with Number Trained",
        mapbox_style="carto-positron",  # Using Mapbox style
        center={"lat": 32.8, "lon": -83.6},  # Adjust this based on your target region
        zoom=5,  # Adjust zoom level as needed
        opacity=0.5  # Adjust opacity for a softer appearance
    )

    # Step 3: Update map layout and properties
    fig.update_layout(
        mapbox=dict(
            style="carto-positron",  # Background style of the map
            zoom=5,  # Control zoom level
            center={"lat": 32.8, "lon": -83.6},  # Center of the map (Georgia)
            pitch=0  # Optional, to remove tilt
        ),
        title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold')
    )

    # Step 4: Print data for debugging (optional)
    print(df)

    return fig


# fig_1 = px.choropleth_map(df, geojson=counties, locations='fips', color='unemp',
#                            color_continuous_scale="Viridis",
#                            range_color=(0, 12),
#                            map_style="carto-positron",
#                            zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
#                            opacity=0.5,
#                            labels={'unemp':'unemployment rate'}
#                           )
# fig_1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


# Step 4: Print data for debugging (optional)
# print(df)

# Set up the bounding box for Georgia to ensure the map is focused only on Georgia
# Georgia latitude and longitude boundaries (approximate)
# georgia_bounds = {
#     "lat": [30.0, 35.5],  # Latitude range
#     "lon": [-85.0, -80.0],  # Longitude range
# }

# fig.update_layout(
#     mapbox=dict(
#         # Focus on Georgia's geographic boundaries
#         pitch=0,
#         zoom=5,
#         center={"lat": 32.8, "lon": -83.6},
#     ),
# )
fig = map_figure()
app.layout = html.Div([
    html.H1("Event Locations Map with Bubble Sizes Based on Number Trained"),
    dcc.Graph(
        id='event-map',
        figure=fig,
        style={'width':'90%','height':'600px'}
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
