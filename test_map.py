import dash
from dash import dcc,html
import plotly.express as px
import pandas as pd
import random
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
import requests

geolocator = Nominatim(user_agent="address_locator")

app = dash.Dash(__name__)

# data = []

# county_coordinates = {
#     "Bibb County": (32.8460, -83.6324),  
#     "Houston County": (32.5292, -83.5920), 
#     "Peach County": (32.8810, -83.5870),  
#     "Monroe County": (33.0364, -83.6017),  
#     "Crawford County": (32.8246, -84.2321),  
#     "Jones County": (33.0701, -83.6689)  
# }

# event_types = [
#     "Macon Magazine Soiree Event", "Camp Hope Mental Wellbeing Event", "Childcare Network - Houston Rd",
#     "Houston Rd Daycare - Houston Rd", "Pharmacy - Kroger - Hartley Bridge Rd", "Pharmacy - CVS - Houston Rd",
#     "Houston County FC Collaborative Meeting", "Pharmacy - CVS - Gray Hwy", "Pharmacy - CVS - Vineville",
#     "Pharmacy - Kroger Tom Hill", "RMG Leadership Meeting", "RMG/CES Proposal Discussion",
#     "Kroger Pharmacy - Presidential Pkwy", "Pharmacy - Walmart - Harrison Rd", "Powell's Pharmacy - Bloomfield Rd",
#     "Wesleyan CCRT Meeting", "Macon Mental Health Matters Alliance", "Resilient Coalition Connection (SWGA + RMG)",
#     "Joshua House - Bloomfield Rd", "Peggies Stay and Play - Bloomfield Rd", "Pharmacy - CVS Bloomfield Rd",
#     "U Save it Pharmacy - Pio Nono Ave", "RMG Leadership Meeting", "Hide and Seek Daycare - Pio Nono",
#     "Latrenda World for Learning - Houston Ave and Bloomfield"
# ]

# counties = ['Bibb County', 'Houston County', 'Peach County', 'Monroe County', 'Crawford County', 'Jones County']
# demographic_info = [
#     "Race/Ethnicity: 70% Black, 20% Hispanic, 10% White", 
#     "Race/Ethnicity: 50% Black, 50% White", 
#     "Gender: 30% Female, 70% Male", 
#     "Age: 60% 65+, 40% 45-60", 
#     "Race/Ethnicity: 80% Black, 10% White, 10% Other", 
#     "Race/Ethnicity: 50% Black, 50% White", 
#     "Gender: 60% Female, 40% Male"
# ]

# identified_gaps = [
#     "Lack of childcare training for workers in low-income areas", 
#     "Lack of specific training on patient communication", 
#     "No training available for elderly on mental health management", 
#     "Lack of disaster preparedness training for rural communities", 
#     "Gap in trauma-informed care for educators and first responders", 
#     "Lack of mental health resources for children and adolescents", 
#     "Need for leadership training in rural areas"
# ]

# population_served_options = [
#     "Children", "Elderly", "Rural Residents", "Low-Income Families", "Teachers and Educators", "Healthcare Professionals", "General Public"
# ]

# street_names = [
#     "Windy Hill Rd SE", "Ponce de Leon Ave", "Peachtree St", "Main St", "Highland Ave",
#     "Chattahoochee Ave", "Cherry St", "Broad St", "Macon St", "Cobb Pkwy", "Spring St",
#     "Johnson Ferry Rd", "Roswell Rd", "Jonesboro Rd", "Old National Hwy", "Buford Hwy"
# ]

# cities = [
#     "Marietta", "Macon", "Atlanta", "Warner Robins", "Peachtree City", "Albany", "Savannah", 
#     "Columbus", "Roswell", "Augusta", "Athens", "Valdosta", "Douglasville", "Sandy Springs"
# ]

# counties = [
#     "Cobb County", "Bibb County", "Fulton County", "Gwinnett County", "DeKalb County",
#     "Clayton County", "Cherokee County", "Henry County", "Richmond County", "Muscogee County"
# ]

# # zip_codes = [
# #     "30067", "31206", "30309", "31088", "31401", "30303", "30064", "30342", "30339", "31204"
# # ]


# # Open the text file and read it
# with open('US.txt', 'r') as file:
#     lines = file.readlines()

# # List to store Georgia postal codes
# georgia_postal_codes = []

# # Iterate through each line in the file
# for line in lines:
#     # Split each line by spaces or tabs (assuming space-separated columns)
#     parts = line.split()

#     # Check if the state is Georgia (GA) and if the postal code is not already in the list
#     if len(parts) >= 6 and parts[3] == 'Georgia' or parts[3] == 'GA': 
#         georgia_postal_codes.append(parts[1])

#     # Stop once we have 100 postal codes for Georgia
#     if len(georgia_postal_codes) == 100:
#         break

# print(georgia_postal_codes)
# # Print the first 100 postal codes
# # for postal_code in georgia_postal_codes:
# #     print(postal_code)
# # Print the first 10 real ZIP codes
# # print(zip_codes[:10])

# def random_date(start_date, end_date):
#     delta = end_date - start_date
#     return start_date + timedelta(days=random.randint(0, delta.days))

# for _ in range(100):
#     event = random.choice(event_types)
#     county = random.choice(counties)
#     # lat, lon = county_coordinates[county]  
#     number_trained = random.randint(10, 200)  
#     demographic = random.choice(demographic_info)  
#     gap = random.choice(identified_gaps)  
#     population_served = random.choice(population_served_options)
#     date = random_date(datetime(2024, 1, 1), datetime(2024, 12, 31)).strftime('%m/%d/%Y')
#         # Generate a random address with realistic street name, city, county, state, and zip code
#     street_name = random.choice(street_names)
#     city = random.choice(cities)
#     zip_code = georgia_postal_codes[_]
#     # print(zip_code)
#     # Format the address to match the required format
#     address = f"{random.randint(1000, 9999)} {street_name}, {city}, {county}, Georgia, {zip_code}"
#     location = geolocator.geocode(zip_code)
#     if location:
#         lat = location.latitude
#         lon = location.longitude
#         # print(f"Address: {address}")
#         # print(f"Latitude: {location.latitude}")
#         # print(f"Longitpude: {location.longitude}")
#     else:
#         print(f"Could not geocode the address: {address}")
#     data.append({
#         'Event Name': event,
#         'County': county,
#         'Address': address,
#         'Latitude': lat,
#         'Longitude': lon,
#         'Event Type': random.choice(["Awareness", "Training", "Drop-In", "Community Connection"]),
#         'Population Served': population_served,
#         'Number Trained': number_trained,
#         'Hours': random.randint(1, 6),
#         'Date': date,  
#         'Demographic Information': demographic,
#         'Identified Gaps': gap
#     })

# df = pd.DataFrame(data)
# # print(df)
from sqlalchemy import create_engine, text


# df = pd.read_excel("synthetic_data_collection_process.xlsx")
# df.to_excel("synthetic_data_collection_process.xlsx", index=False)


def get_db_connection():
    server = 'my-sql-dbserver.database.windows.net'
    database = 'mydb'
    username = 'Sarif748'
    password = 'Sa%408790883008'
    db_connection_str = (
        f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+18+for+SQL+Server"
    )
    try:
        engine = create_engine(db_connection_str)
        with engine.connect() as conn:
            print("Connection successful")
        return engine
    except Exception as e:
        print(f"Error: {e}")
        return None


def map_figure():
    conn = get_db_connection()
    if conn:
        query = "SELECT * FROM Events"
        df = pd.read_sql(query, conn)
        print(df)

    fig = px.choropleth_mapbox(
        df, 
        geojson=None,  # Replace None with your custom GeoJSON or use default mapbox boundaries
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

# Step 4: Print data for debugging (optional)
# print(df)

# Set up the bounding box for Georgia to ensure the map is focused only on Georgia
# Georgia latitude and longitude boundaries (approximate)
georgia_bounds = {
    "lat": [30.0, 35.5],  # Latitude range
    "lon": [-85.0, -80.0],  # Longitude range
}

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




