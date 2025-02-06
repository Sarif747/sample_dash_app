from urllib.request import urlopen
import json
import dash
from matplotlib.patches import Polygon
import pandas as pd
import plotly.express as px
from dash import dcc, html
from sqlalchemy import create_engine

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
    df_2 = pd.read_sql(query, conn)
    print(df_2)

# Load GeoJSON data for counties
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

georgia_counties = {
    "type": "FeatureCollection",
    "features": [county for county in counties['features'] if county['properties']['STATE'] == '13']
}
print(georgia_counties)
for feature in counties['features'][:1]:  # Only check the first feature
    print(feature['properties'])
# Extract county names and FIPS codes (ID) for Georgia counties
county_data = []

for feature in georgia_counties['features']:
    county_name = feature['properties']['NAME']
    county_id = feature['properties']['GEO_ID'] 
    
    # You can also get coordinates if you need them
    coordinates = feature['geometry']['coordinates'][0]  # Assuming it's a simple polygon
    county_data.append({
        'County': county_name,
        'County_ID': county_id,
        'Coordinates': coordinates
    })

# Convert the county data to a DataFrame for easy manipulation
df_georgia_counties = pd.DataFrame(county_data)
# Step 1: Ensure geo_id is treated as a string for slicing
df_georgia_counties['County_ID'] = df_georgia_counties['County_ID'].astype(str)

# Step 2: Extract the last five digits of geo_id
df_georgia_counties['County_ID'] = df_georgia_counties['County_ID'].str[-5:]

# Step 3: Convert geo_id_last_5 to integer
df_georgia_counties['County_ID'] = df_georgia_counties['County_ID'].astype(int)
# Print the DataFrame
print(df_georgia_counties)

# print(df_2)
df_2['County'] = df_2['County'].str.replace(' County$', '', regex=True)
merged_df = pd.merge(df_2, df_georgia_counties, on='County', how='left')
print(merged_df)

df_1 = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv", dtype={"fips": str})

def map_graph():
    # Correct the function name to choropleth_mapbox
    fig = px.choropleth_mapbox(df_1, geojson=georgia_counties, locations='fips', color='unemp',
                                color_continuous_scale="Viridis",
                                range_color=(0, 12),
                                mapbox_style="open-street-map",  # No Mapbox access token needed for this style
                                zoom=6,
                                center={"lat": 33.0, "lon": -83.5},
                                opacity=0.5,
                                labels={'unemp': 'Unemployment Rate'})
    
    # Remove margins
    fig.update_layout(margin={"r":0, "t":0, "l":0, "b":0})

    return fig

def map_graph_1():
    # Correct the function name to choropleth_mapbox
    if conn:
        query = "SELECT * FROM Events"
        df = pd.read_sql(query, conn)
        print(df)
    fig = px.choropleth_mapbox(merged_df, geojson=georgia_counties, locations='County_ID', color='Event_Type',
                                color_continuous_scale="Viridis",
                                range_color=(0, 12),
                                mapbox_style="open-street-map",
                                hover_data={
                                    "County": True, 
                                    "Number_Trained": True, 
                                    "Hours": True, 
                                    "Date": True,
                                    "Address": True, 
                                    "Population_Served": True, 
                                    "Demographic_Information": True, 
                                    "Identified_Gaps": True, 
                                },  # No Mapbox access token needed for this style
                                zoom=6, 
                                center={"lat": 33.0, "lon": -83.5},
                                opacity=0.5,
                                labels={'unemp': 'Unemployment Rate'})
    
    # Remove margins
    fig.update_layout(margin={"r":0, "t":0, "l":0, "b":0})

    return fig

# Generate the figure using map_graph function
fig = map_graph()
fig_1 = map_graph_1()
# Dash layout with the graph
app.layout = html.Div([
    html.H1("Event Locations Map with Bubble Sizes Based on Number Trained"),
    dcc.Graph(
        id='event-map',
        figure=fig,
        style={'width': '90%', 'height': '600px'}
    ),
    dcc.Graph(
        id='event-map',
        figure=fig_1,
        style={'width': '90%', 'height': '600px'}
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
