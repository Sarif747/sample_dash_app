import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import base64
import io
import mysql
from sqlalchemy import create_engine, text
import mysql.connector
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from geopy.geocoders import Nominatim
from dash.exceptions import PreventUpdate
import dash
from dash import dcc,html
import plotly.express as px
import pandas as pd
import random
from datetime import datetime, timedelta
import requests
import openai
import re
import cx_Oracle
from datetime import datetime
from dotenv import load_dotenv
import os

geolocator = Nominatim(user_agent="address_locator")


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True, prevent_initial_callbacks='initial_duplicate')

load_dotenv()  # Load environment variables from the .env file

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(OPENAI_API_KEY)

openai.api_key = OPENAI_API_KEY
# openai.api_key = "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"

user_table = "events"
user_column_event_name = "event_name"
user_column_county = "county"
user_column_address = "address"
user_column_event_type = "event_type"
user_column_population_served = "population_served"
user_column_number_trained = "number_trained"
user_column_hours = "hours"
user_column_event_date = "event_date"
user_column_demographic_info = "demographic_info"
user_column_identified_gaps = "identified_gaps"

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
        with engine.connect() as conn:
            print("Connection successful")
        return engine
    except Exception as e:
        print(f"Error: {e}")
        return None

# def get_db_connection():
#     try:
#         connection = cx_Oracle.connect(
#             user='system',    
#             password='orcl', 
#             dsn='localhost:1521/orcl'           
#         )
#         print("Connection successful!")
#         return connection
#     except cx_Oracle.Error as e:
#         error, = e.args
#         print(f"Error connecting to Oracle: {error.code}, {error.message}")
#         return None

def geo_codes(address):
    address_parts = address.split(',')
    if len(address_parts) >= 4:
        fourth_element = address_parts[4].strip()
        print(fourth_element)
        geolocator = Nominatim(user_agent="myGeocoder")
        location = geolocator.geocode(fourth_element)
        lat = location.latitude
        lon = location.longitude
        return lat,lon

def map_figure():
    conn = get_db_connection()
    if conn:
        query = "SELECT * FROM Events"
        df = pd.read_sql(query, conn)

    fig = px.scatter_mapbox(df, 
                            lat="Latitude", 
                            lon="Longitude", 
                            color="Event_Type", 
                            size="Number_Trained",  
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
                            color_discrete_map={"Awareness": "blue", "Training": "green", "Drop-In": "red", "Community Connection": "purple"},
                            size_max=20, 
                            title="Event Locations with Bubble Sizes Based on Number Trained")

    fig.update_layout(
        mapbox_style="carto-positron",  
        mapbox_center={"lat": 32.8, "lon": -83.6},  
        mapbox_zoom=5,  
        title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold') 

    )

    fig.update_layout(
        mapbox=dict(
            pitch=0,
            zoom=5,
            center={"lat": 32.8, "lon": -83.6},
        ),
    )
    print(df)
    return fig

georgia_bounds = {
    "lat": [30.0, 35.5],  
    "lon": [-85.0, -80.0], 
}

def data_manipulation():
    return html.Div([
        html.Div([
        dbc.Row([
            html.H3("Select the Database you want to work on",style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
            dbc.Col(
                dcc.Dropdown(id='db_dropdown', options=['mydb', 'resilient_db_1', 'resilient_db_2'], value='',style={
                                    'width': '300px',
                                    'height': '40px',
                                    'marginLeft': '25px',
                                    'textAlign': 'center',
                                    'color': 'darkgreen',
                                }            
                            ),
            ),
            dbc.Col(
                dbc.Button("Generate Report", id="report_button", n_clicks=0, style={
                    "position": "absolute", 
                    "top": "100px",  
                    "right": "20px",  
                    "color": "white", 
                    "backgroundColor": "darkgreen"
                },)
            )
        ])
    ]),
    html.H1("Event Locations in georgia map happen over the years",style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
    html.H4("This map highlights the events and their respective details like date, address, population serverd and demographic info. It also highlights the gaps in thoes areas where intervention and training is needed",style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
    html.Div([
        dcc.Graph(
            id='event-map',
            figure=map_figure(),
            style={'width':'90%','height':'600px'}
        )
    ],style={
                            'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                            'borderRadius': '10px',
                            'padding': '10px',
                            'backgroundColor': 'white',
                            'margin': '20px auto',
                            'width': '100%',
                        }),
    html.H1("Event Data Submission with File Upload",style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
    html.H4("In this Upload section you can upload an excel or csv file with large amount of data directly",style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
    html.Div([
        html.H4("Upload CSV or Excel File",style={'textAlign': 'left', 'marginLeft': '20px', 'color': 'darkgreen'}),
        dcc.Upload(
            id='upload-data',
            children=html.Button('Upload File'),
            multiple=False,
            style={
                            'width': '200px',
                            'height': '40px',
                            'textAlign': 'center',
                            'color': 'darkgreen',
                }
        ),
        dbc.Button("Submit Data", id="submit-button", n_clicks=0, style={"margin-top": "20px",'color': 'white',"backgroundColor": "darkgreen"}),
        html.Div(id='output-data-upload', style={'margin-top': '10px'})
    ],style={
                            'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                            'borderRadius': '10px',
                            'padding': '10px',
                            'backgroundColor': 'white',
                            'margin': '20px auto',
                            'width': '100%',
                        },),

    html.Div(id='data-table-container', style={'padding': '20px'}),
    html.Div(id='final-submission'),
    html.Div([
        html.H4("Enter Event Data Manually",style={'textAlign': 'left', 'marginLeft': '20px', 'color': 'darkgreen'}),
        html.H5("In this form you can enter the data manually for each record",style={'textAlign': 'left', 'marginLeft': '20px', 'color': 'darkgreen'}),
        dbc.Row([
            dbc.Col([
                dbc.Label("Event Name",style={'textAlign': 'left', 'marginLeft': '20px', 'color': 'darkgreen'}),
                dbc.Input(id="event-name", type="text", placeholder="Enter event name",style={'color': 'darkgreen'}),
            ], width=6),
            dbc.Col([
                dbc.Label("County",style={'textAlign': 'left', 'marginLeft': '20px', 'color': 'darkgreen'}),
                dbc.Input(id="county", type="text", placeholder="Enter county",style={'color': 'darkgreen'}),
            ], width=6),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Label("Address",style={'textAlign': 'left', 'marginLeft': '20px', 'color': 'darkgreen'}),
                dbc.Input(id="address", type="text", placeholder="Enter Address (e.g., 2401 Windy Hill RD SE, Marietta, Georgia, 30067)",style={'color': 'darkgreen'}),
            ], width=6),
            dbc.Col([
                dbc.Label("Population Served",style={'textAlign': 'left', 'marginLeft': '20px', 'color': 'darkgreen'}),
                dbc.Input(id="population-served", type="text", placeholder="Enter population served",style={'color': 'darkgreen'}),
            ], width=6),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Label("Event Type",style={'textAlign': 'left', 'marginLeft': '20px', 'color': 'darkgreen'}),
                dbc.Input(id="event-type", type="text", placeholder="Enter event type (e.g., Training, Awareness)",style={'color': 'darkgreen'}),
            ], width=6),
            dbc.Col([
                dbc.Label("Number Trained",style={'textAlign': 'left', 'marginLeft': '20px', 'color': 'darkgreen'}),
                dbc.Input(id="number-trained", type="number", placeholder="Enter number of people trained",style={'color': 'darkgreen'}),
            ], width=6),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Label("Hours",style={'textAlign': 'left', 'marginLeft': '20px', 'color': 'darkgreen'}),
                dbc.Input(id="hours", type="number", placeholder="Enter event duration in hours",style={'color': 'darkgreen'}),
            ], width=6),
            dbc.Col([
                dbc.Label("Date",style={'textAlign': 'left', 'marginLeft': '20px', 'color': 'darkgreen'}),
                dbc.Input(id="event-date", type="date", placeholder="Select event date",style={'color': 'darkgreen'}),
            ], width=6),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Label("Demographic Information",style={'textAlign': 'left', 'marginLeft': '20px', 'color': 'darkgreen'}),
                dbc.Input(id="demographic-info", type="text", placeholder="Enter demographic info (e.g., Age, Race, Gender)",style={'color': 'darkgreen'}),
            ], width=6),
            dbc.Col([
                dbc.Label("Identified Gaps",style={'textAlign': 'left', 'marginLeft': '20px', 'color': 'darkgreen'}),
                dbc.Input(id="identified-gaps", type="text", placeholder="Enter identified gaps (e.g., lack of training)",style={'color': 'darkgreen'}),
            ], width=6),
        ]),
        dbc.Button("Submit Data", id="submit-form-button", n_clicks=0, style={"margin-top": "20px",'color': 'white',"backgroundColor": "darkgreen"},)
    ], style={
                            'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                            'borderRadius': '10px',
                            'padding': '10px',
                            'backgroundColor': 'white',
                            'margin': '20px auto',
                            'width': '100%',
                        },),
    html.Div(id='output-data-upload_1', style={'margin-top': '10px'}),
    html.Div(id='data-table-container_1', style={'padding': '20px'}),
    html.Div([
        html.H4("Search for Event Data",style={'textAlign': 'left', 'marginLeft': '20px', 'color': 'darkgreen'}),
        html.H5("You can search the data by entering the event name or event date and you can also update and delete the specific search record manually",style={'textAlign': 'left', 'marginLeft': '20px', 'color': 'darkgreen'}),
        dbc.Row([
            dbc.Col([
                dbc.Label("Event Name",style={'textAlign': 'left', 'marginLeft': '20px', 'color': 'darkgreen'}),
                dbc.Input(id="search-event-name", type="text", placeholder="Enter event name to search",style={'color': 'darkgreen'}),
            ], width=6),
            dbc.Col([
                dbc.Label("Event Date",style={'textAlign': 'left', 'marginLeft': '20px', 'color': 'darkgreen'}),
                dbc.Input(id="search-event-date", type="date", placeholder="Enter event date to search",style={'color': 'darkgreen'}),
            ], width=6),
        ]),
    ],style={
                            'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                            'borderRadius': '10px',
                            'padding': '10px',
                            'backgroundColor': 'white',
                            'margin': '20px auto',
                            'width': '100%',
                        },),
    html.Div(id="search-output", style={"margin-top": "20px"}),
    html.Div(id='search-results-container'),
    html.Div(id="update-feedback", style={"margin-top": "20px"}),
    dcc.Store(id="modal-state", data=False),
    dcc.Store(id="modal-state_2",data=False),
    html.Div(id="modal-container"),
    html.Div(id='modal-container_2'),
    html.H1("Ask your query",style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
    html.H5("In this Text box area user can enter there their request for specific data",style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
    html.Div([dbc.Row([
        dcc.Textarea(
            id='user-input',
            style={'textAlign': 'left', 'marginLeft': '20px', 'color': 'darkgreen','width':'97%','height':100},
            placeholder="Enter your query here, e.g., 'Show me all users with age greater than 30'",
        ),]),
        dbc.Button('submit', id='convert-button', n_clicks=0,style={"margin-top": "40px",'color': 'white',"backgroundColor": "darkgreen"}),
    ],style={
                            'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                            'borderRadius': '10px',
                            'padding': '10px',
                            'backgroundColor': 'white',
                            'margin': '20px auto',
                            'width': '100%',
                        }),
    html.Div(id='sql-output', style={'marginTop': '20px'}),
    html.Div(id='query-result', style={'marginTop': '20px'})
],style={'backgroundColor': 'lightgreen', 'padding': '20px'})

# @app.callback(
#     Output('data-table-container', 'children', allow_duplicate=True),
#     Output('output-data-upload', 'children'),
#     Input('upload-data', 'contents'),
#     State('upload-data', 'filename')
# )
def upload_file_2(contents, filename):
    if contents is None:
        return [], " "
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            return html.Div(dash_table.DataTable(
                id='uploaded-table',
                columns=[{"name": col, "id": col} for col in df.columns],
                data=df.to_dict('records'),
                page_size=10,  
                style_table={
                'width': '100%',  
                'overflowX': 'auto',  
                'maxHeight': '400px',  
                'marginTop': '20px'  
                },
                style_cell={
                    'textAlign': 'center',
                    'padding': '10px',
                    'fontSize': '14px',
                    'color': 'darkgreen'
                },
                style_header={
                    'backgroundColor': '#f4f4f4',  
                    'fontWeight': 'bold',  
                    'textAlign': 'center' 
                },
                style_data={
                    'whiteSpace': 'normal',  
                    'overflow': 'hidden' 
                },
                style_data_conditional=[
                                {
                                    'if': {
                                        'row_index': 'odd'
                                    },
                                    'backgroundColor': '#f1f1f1'
                                }
                            ],
            ),style={
                            'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                            'borderRadius': '10px',
                            'padding': '10px',
                            'backgroundColor': 'white',
                            'margin': '20px auto',
                            'width': '100%',
                        },
            ), f"CSV File '{filename}' successfully uploaded!"
        elif filename.endswith('.xlsx') or filename.endswith('.xls'):
            df = pd.read_excel(io.BytesIO(decoded))
            return html.Div(dash_table.DataTable(
                id='uploaded-table',
                columns=[{"name": col, "id": col} for col in df.columns],
                data=df.to_dict('records'),
                page_size=10, 
                style_table={
                    'width': '100%',  
                    'overflowX': 'auto',  
                    'maxHeight': '400px',  
                    'marginTop': '20px'  
                },
                style_cell={
                    'textAlign': 'center',
                    'padding': '10px',
                    'fontSize': '14px',
                    'color': 'darkgreen'
                },
                style_header={
                    'backgroundColor': '#f4f4f4',  
                    'fontWeight': 'bold',  
                    'textAlign': 'center' 
                },
                style_data={
                    'whiteSpace': 'normal',  
                    'overflow': 'hidden' 
                },
                style_data_conditional=[
                                {
                                    'if': {
                                        'row_index': 'odd'
                                    },
                                    'backgroundColor': '#f1f1f1'
                                }
                            ],
            ),style={
                            'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                            'borderRadius': '10px',
                            'padding': '10px',
                            'backgroundColor': 'white',
                            'margin': '20px auto',
                            'width': '100%',
                        },
            ), f"Excel File '{filename}' successfully uploaded!"

        else:
            return [], "Unsupported file type. Please upload a CSV or Excel file."

    except Exception as e:
        return [], f"Error processing file: {str(e)}"

# @app.callback(
#     Output("modal-container", "children"),
#     Output("modal-state", "data", allow_duplicate=True),
#     Input("submit-button", "n_clicks"),
#     State('upload-data', 'contents'),
#     State('data-table-container', 'children'),
#     prevent_initial_call=True
# )
def show_modal(n_clicks,contents, table):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    confirm_clicks = 0
    if trigger_id == "submit-button" and n_clicks > 0 and table is not None:
        # print(table)
        # table_data = table['props']['data']
        table_data = table['props']['children']['props']['data']
        # table_data = table
        # print(table_data)
        dash_table_in_modal = html.Div(dash_table.DataTable(
            id='confirmation-table',
            columns=[{"name": col, "id": col} for col in table_data[0].keys()],
            data=table_data,
            page_size=10,
            style_table={
                'width': '100%',  
                'overflowX': 'auto',  
                'maxHeight': '400px',  
                'marginTop': '20px'  
            },
            style_cell={
                'textAlign': 'center',
                'padding': '10px',
                'fontSize': '14px',
                'color': 'darkgreen'
            },
            style_header={
                'backgroundColor': '#f4f4f4',  
                'fontWeight': 'bold',  
                'textAlign': 'center' 
            },
            style_data={
                'whiteSpace': 'normal',  
                'overflow': 'hidden' 
            },
            style_data_conditional=[
                            {
                                'if': {
                                    'row_index': 'odd'
                                },
                                'backgroundColor': '#f1f1f1'
                            }
                        ],
            ),style={
                        'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                        'borderRadius': '10px',
                        'padding': '10px',
                        'backgroundColor': 'white',
                        'margin': '20px auto',
                        'width': '100%',
                    },)
        modal = dbc.Modal(
            [
                dbc.ModalHeader("Confirm Your Submission"),
                dbc.ModalBody([
                    html.H5("Please review the data before submitting:"),
                    dash_table_in_modal
                ]),
                dbc.ModalFooter([
                    dbc.Button("Confirm", id="confirm-submit-button", style={"margin-top": "20px",'color': 'white',"backgroundColor": "darkgreen"})
                ])
            ],
            is_open=True,
            size="lg",  
            style={"maxWidth": "100%"}  
        )
        return modal, True

    if trigger_id == "confirm-submit-button" and confirm_clicks > 0:
        return [], False
    return [], False

# @app.callback(
#     Output('final-submission', 'children'),
#     Output("modal-state", "data", allow_duplicate=True),
#     Input("confirm-submit-button", "n_clicks"),
#     State('data-table-container', 'children') 
# )
def final_submission(n_clicks, table):
    if n_clicks is not None and n_clicks > 0:
        if table is None or len(table['props']['children']['props']['data']) == 0:
            return "No data to submit", True
        
        data = table['props']['children']['props']['data']
        
        engine = get_db_connection()
        if engine is None:
            return "Error: Unable to connect to the database.", True
        
        new_data = []
        with engine.connect() as conn:

            for record in data:
                try:
                    # Convert date
                    event_date = record.get('Date')
                    date_object = datetime.strptime(event_date, '%m/%d/%Y') if event_date else None
                    
                    # Prepare the insert query
                    insert_query = text("""
                    INSERT INTO events (
                        Event_Name, County, Address, Latitude, Longitude, 
                        Event_Type, Population_Served, Number_Trained, 
                        Hours, Date, Demographic_Information, Identified_Gaps
                    ) VALUES (
                        :event_name, :county, :address, :latitude, :longitude, 
                        :event_type, :population_served, :number_trained, 
                        :hours, :date, :demographic_info, :identified_gaps
                    )
                    """)
                    
                    # Prepare the values, handling potential None/empty values
                    values = {
                        'event_name': record.get('Event Name', ''),
                        'county': record.get('County', ''),
                        'address': record.get('Address', ''),
                        'latitude': float(record.get('Latitude', 0)) if record.get('Latitude') else None,
                        'longitude': float(record.get('Longitude', 0)) if record.get('Longitude') else None,
                        'event_type': record.get('Event Type', ''),
                        'population_served': record.get('Population Served', ''),
                        'number_trained': int(record.get('Number Trained', 0)) if record.get('Number Trained') else None,
                        'hours': int(record.get('Hours', 0)) if record.get('Hours') else None,
                        'date': date_object,
                        'demographic_info': record.get('Demographic Information', ''),
                        'identified_gaps': record.get('Identified Gaps', '')
                    }
                    
                    # Check for duplicate before inserting
                    select_query = text("""
                    SELECT * FROM events 
                    WHERE Event_Name = :event_name AND Date = :date
                    """)
                    
                    with conn.begin() as transaction:
                        # Check for duplicate
                        result = conn.execute(select_query, values).fetchone()
                        
                        if not result:
                            # Execute the insert
                            conn.execute(insert_query, values)
                            conn.commit()
                            new_data.append(record)
                
                except Exception as e:
                    print(f"Error processing record: {record}")
                    print(f"Error details: {str(e)}")
                    continue
        
        if new_data:
            return html.Div(html.P(f"{len(new_data)} new records submitted successfully.")), False
        else:
            return "No new data to submit.", False

    return "", False

# @app.callback(
#     [Output('modal-container_2', 'children'),
#      Output('modal-state_2', 'data')],
#     Input('submit-form-button', 'n_clicks'),
#     [State('event-name', 'value'),
#      State('county', 'value'),
#      State('address', 'value'),
#      State('population-served', 'value'),
#      State('event-type', 'value'),
#      State('number-trained', 'value'),
#      State('hours', 'value'),
#      State('event-date', 'value'),
#      State('demographic-info', 'value'),
#      State('identified-gaps', 'value'),],
#     prevent_initial_call=True
# )
def show_modal_2(n_clicks,event_name, county, address, population_served, event_type, number_trained, hours, event_date, demographic_info, identified_gaps):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    confirm_clicks =0
    if trigger_id == "submit-form-button" and n_clicks and n_clicks > 0:
        data = {
            "Event Name": [event_name],
            "County": [county],
            "Address": [address],
            "Population Served": [population_served],
            "Event Type": [event_type],
            "Number Trained": [number_trained],
            "Hours": [hours],
            "Event Date": [event_date],
            "Demographic Info": [demographic_info],
            "Identified Gaps": [identified_gaps]
        }
        df = pd.DataFrame(data)

        dash_table_in_modal = html.Div(dash_table.DataTable(
            id='confirmation-table',
            columns=[{"name": col, "id": col} for col in df.columns],
            data=df.to_dict('records'),
            page_size=10,
            style_table={
                'width': '100%',  
                'overflowX': 'auto',  
                'maxHeight': '400px',  
                'marginTop': '20px'  
            },
            style_cell={
                'textAlign': 'center',
                'padding': '10px',
                'fontSize': '14px',
                'color': 'darkgreen'
            },
            style_header={
                'backgroundColor': '#f4f4f4',  
                'fontWeight': 'bold',  
                'textAlign': 'center' 
            },
            style_data={
                'whiteSpace': 'normal',  
                'overflow': 'hidden' 
            },
            style_data_conditional=[
                            {
                                'if': {
                                    'row_index': 'odd'
                                },
                                'backgroundColor': '#f1f1f1'
                            }
                        ],
             ),style={
                        'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                        'borderRadius': '10px',
                        'padding': '10px',
                        'backgroundColor': 'white',
                        'margin': '20px auto',
                        'width': '100%',
                    },)

        modal = dbc.Modal(
            [
                dbc.ModalHeader("Confirm Your Submission"),
                dbc.ModalBody([
                    html.H5("Please review the data before submitting:"),
                    dash_table_in_modal
                ]),
                dbc.ModalFooter([
                    dbc.Button("Confirm", id="confirm-submit-button-2", style={"margin-top": "20px",'color': 'white',"backgroundColor": "darkgreen"}, n_clicks=0)
                ])
            ],
            id="confirmation-modal",
            is_open=True,
            size="lg",
            style={"maxWidth": "90%"}
        )

        return modal, True
    # Close modal when confirm is clicked
    if trigger_id == "confirm-submit-button-2" and confirm_clicks and confirm_clicks > 0:
        return [], False

    return None, False

# @app.callback(
#     Output('output-data-upload_1', 'children'),
#     Input('confirm-submit-button-2', 'n_clicks'),
#     [State('event-name', 'value'),
#      State('county', 'value'),
#      State('address', 'value'),
#      State('population-served', 'value'),
#      State('event-type', 'value'),
#      State('number-trained', 'value'),
#      State('hours', 'value'),
#      State('event-date', 'value'),
#      State('demographic-info', 'value'),
#      State('identified-gaps', 'value'),
#      State('modal-state_2', 'data')]
# )
def submit_data(confirm_clicks, event_name, county, address, population_served, event_type, number_trained, hours, event_date, demographic_info, identified_gaps, modal_state):
    if confirm_clicks and confirm_clicks > 0 and modal_state:
        try:
            latitude, longitude = geo_codes(address)
            print(f"Geocode results: {latitude}, {longitude}")
            engine = get_db_connection()
            print("Database connection successful!")
            print(event_date)
            
            # Convert the event_date to a datetime object
            date_obj = datetime.strptime(event_date, '%Y-%m-%d')
            formatted_date = date_obj.strftime('%m/%d/%Y')
            date_object = datetime.strptime(formatted_date, '%m/%d/%Y') if event_date else None
            print(date_object)
            print(formatted_date)
            
            if engine is None:
                return "Error: Unable to connect to the database.", True
            
            with engine.connect() as conn:
                # Correct the placeholder format for SQLAlchemy
                insert_query = text("""
                INSERT INTO events (
                    Event_Name, County, Address, Latitude, Longitude, 
                    Event_Type, Population_Served, Number_Trained, 
                    Hours, Date, Demographic_Information, Identified_Gaps
                ) VALUES (
                    :event_name, :county, :address, :latitude, :longitude, 
                    :event_type, :population_served, :number_trained, 
                    :hours, :date, :demographic_info, :identified_gaps
                )
                """)
                
                # Define the values to be inserted as a dictionary
                values = {
                    'event_name': event_name,
                    'county': county,
                    'address': address,
                    'latitude': latitude,
                    'longitude': longitude,
                    'event_type': event_type,
                    'population_served': population_served,
                    'number_trained': number_trained,
                    'hours': hours,
                    'date': date_object,
                    'demographic_info': demographic_info,
                    'identified_gaps': identified_gaps
                }
                
                # Modify the select query to match the parameter format
                select_query = text("""
                SELECT * FROM Events 
                WHERE Event_Name = :event_name AND Date = :date
                """)
                
                # Execute the select query and check for duplicates
                result = conn.execute(select_query, {'event_name': event_name, 'date': date_object}).fetchone()
                
                # If no result, execute the insert query
                if not result:
                    conn.execute(insert_query, values)
                    conn.commit()
                    print("Data successfully inserted!")
                    return "Data has been successfully submitted."
                
                return "Duplicate event data found, no new data submitted."
        
        except Exception as e:
            return f"Error submitting data: {str(e)}"

    return ""

    
# @app.callback(
#     Output('search-results-container', 'children'),
#     Output('search-output', 'children'),
#     Input('search-event-name', 'value'),
#     Input('search-event-date', 'value')
# )
def search_event_data(event_name, event_date):
    if not event_name and not event_date:
        return '',''
    query = "" 
    params = {}

    if event_name:
        query = text("""SELECT * FROM events WHERE Event_Name LIKE :EVENT_NAME""")
        params = {"EVENT_NAME":event_name}

    if event_date:
        try:
            date_obj = datetime.strptime(event_date, '%Y-%m-%d')
            formatted_date = date_obj.strftime('%m/%d/%Y')
            date_object = datetime.strptime(formatted_date, '%m/%d/%Y') if event_date else None
            query = text("""SELECT * FROM EVENTS WHERE DATE = :EVENT_DATE""")
            params = {"EVENT_DATE":date_object}
        except ValueError:
            return '', html.Div("Invalid date format. Please use MM/DD/YYYY.")

    try:
        engine = get_db_connection()
        if engine is None:
            return '', html.Div("Error: Unable to connect to the database.")
        with engine.connect() as conn:

            result = conn.execute(query, params)
            records = result.fetchall()
            if records:
                columns = ['Event_Name', 'County', 'Address', 'Latitude', 'Longitude', 'Event_Type', 'Population_Served', 'Number_Trained', 'Hours', 'Date', 'Demographic_Information', 'Identified_Gaps']
                df = pd.DataFrame(records, columns=columns)
                # df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')
                data = df.to_dict('records')
                return html.Div(dash_table.DataTable(
                    id='search-results-table',
                    columns=[{"name": col, "id": col} for col in columns],
                    data=data,
                    editable=True,  
                    row_deletable=True, 
                    style_table={
                    'width': '100%',  
                    'overflowX': 'auto',  
                    'maxHeight': '400px',  
                    'marginTop': '20px'  
                },
                style_cell={
                    'textAlign': 'center',
                    'padding': '10px',
                    'fontSize': '14px',
                    'color': 'darkgreen'
                },
                style_header={
                    'backgroundColor': '#f4f4f4',  
                    'fontWeight': 'bold',  
                    'textAlign': 'center' 
                },
                style_data={
                    'whiteSpace': 'normal',  
                    'overflow': 'hidden' 
                },
                style_data_conditional=[
                                {
                                    'if': {
                                        'row_index': 'odd'
                                    },
                                    'backgroundColor': '#f1f1f1'
                                }
                            ],
                ),style={
                            'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                            'borderRadius': '10px',
                            'padding': '10px',
                            'backgroundColor': 'white',
                            'margin': '20px auto',
                            'width': '100%',
                        },), ''  
            else:
                return '', html.Div("No matching events found.")

    except Exception as e:
        return '', html.Div(f"Error while searching: {str(e)}")

# @app.callback(
#     Output("update-feedback", "children"),
#     Input("search-results-table", "data"),
#     State("search-results-table", "data_previous"),
# )
def update_or_delete_data(current_data, previous_data):
    if not previous_data:
        raise PreventUpdate  # Prevent update if there's no previous data
    
    if current_data == previous_data:
        print('Current data is the same as previous data.')
        return "No changes detected."
    
    else:
        print('Current data is different from previous data.')
        try:
            if previous_data is None:
                previous_data = []

            engine = get_db_connection()
            if engine is None:
                return "Error: Unable to connect to the database."

            update_query = text("""
                UPDATE events
                SET County = :COUNTY, Address = :ADDRESS, Latitude = :LATITUDE, Longitude = :LONGITUDE, 
                    Event_Type = :EVENT_TYPE, Population_Served = :POPULATION_SERVED, 
                    Number_Trained = :NUMBER_TRAINED, Hours = :HOURS, Demographic_Information = :DEMOGRAPHIC_INFO, 
                    Identified_Gaps = :IDENTIFIED_GAPS
                WHERE Event_Name = :EVENT_NAME AND Date = :EVENT_DATE
            """)

            delete_query = text("""
                DELETE FROM events WHERE Event_Name = :EVENT_NAME AND Date = :EVENT_DATE
            """)

            with engine.connect() as conn:

                # Case where the number of rows has changed (i.e., some rows might have been deleted)
                if len(current_data) != len(previous_data):
                    deleted_rows = [row for row in previous_data if row not in current_data]
                    for deleted_row in deleted_rows:
                        print(f"Deleted Row: {deleted_row}")
                        event_date = deleted_row["Date"]
                        
                        # Clean up the date format (if necessary)
                        # date_object = datetime.strptime(event_date, '%m/%d/%Y') if event_date else None
                        date_object = datetime.strptime(event_date.split(' ')[0], '%Y-%m-%d').date() if event_date else None

                        # Prepare parameters for deletion
                        params_delete = {
                            "EVENT_NAME": deleted_row["Event_Name"],
                            "EVENT_DATE": date_object
                        }
                        print(f"Deleting row with parameters: {params_delete}")
                        conn.execute(delete_query, params_delete)
                    conn.commit()
                    output = 'Data has been successfully deleted.'
                    return html.Div(output)
                # Case where no rows were deleted, so we perform updates
                else:
                    for row in current_data:
                        # Find the corresponding previous row based on Event_Name and Date
                        previous_row = next((r for r in previous_data if r["Event_Name"] == row["Event_Name"] and r["Date"] == row["Date"]), None)
                        
                        if previous_row:
                            # Check if any data has changed in the row
                            if any(previous_row[key] != row[key] for key in previous_row):
                                print(f"Updating row: {row}")
                                event_date = row["Date"]
                                
                                # Parse the date to match SQL Server format
                                # date_object = datetime.strptime(event_date, '%m/%d/%Y') if event_date else None
                                date_object = datetime.strptime(event_date.split(' ')[0], '%Y-%m-%d').date() if event_date else None

                                # Prepare parameters for the update query
                                params_update = {
                                    "EVENT_NAME": row["Event_Name"],
                                    "COUNTY": row["County"],
                                    "ADDRESS": row["Address"],
                                    "LATITUDE": row["Latitude"],
                                    "LONGITUDE": row["Longitude"],
                                    "EVENT_TYPE": row["Event_Type"],
                                    "POPULATION_SERVED": row["Population_Served"],
                                    "NUMBER_TRAINED": row["Number_Trained"],
                                    "HOURS": row["Hours"],
                                    "EVENT_DATE": date_object,
                                    "DEMOGRAPHIC_INFO": row["Demographic_Information"],
                                    "IDENTIFIED_GAPS": row["Identified_Gaps"]
                                }
                                print(f"Updating row with parameters: {params_update}")
                                conn.execute(update_query, params_update)
                                output = "Data has been successfully updated."

                    conn.commit()
                
                return html.Div(output)      
        except Exception as e:
            return f"Error while updating/deleting: {str(e)}"
        

def return_sql_statment(description):
        messages = [
            {"role": "system", "content": "You are a helpful assistant that generates statistical summaries."},
            {"role": "user", "content": f"convert it into mssql statement: {description}"}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=messages,
            max_tokens=200,  
            temperature=1.0, 
        )
        sql_query = response['choices'][0]['message']['content'].strip()
        print(sql_query)
        sql_query_match = re.search(r"SELECT[\s\S]+?;", sql_query)
        if sql_query_match:
            sql_query = sql_query_match.group(0).strip()
            print("Original SQL query:")
            print(sql_query)
            sql_query_updated = sql_query.replace("events", user_table) \
                                        .replace("eventName", user_column_event_name) \
                                        .replace("eventDate", user_column_event_date) \
                                        .replace("eventType",user_column_event_type) \
                                        .replace("populationServed", user_column_population_served) \
                                        .replace("numberTrained",user_column_number_trained) \
                                        .replace("demographicInfo",user_column_demographic_info) \
                                        .replace("identifiedGaps",user_column_identified_gaps) \
                                        .replace("YourTableName",user_table) \
                                        .replace("EventDate",user_column_event_date) \
                                        .replace("EventName",user_column_event_name) \
                                        .replace("county",user_column_county) \
                                        .replace("your_table_name",user_table) \
                                        .replace("population_data",user_column_population_served) \
                                        .replace("event_data",user_table)
            
            print("\nUpdated SQL query with user-specific table and column names:")
            print(sql_query_updated)
            return sql_query_updated
        else:
            print("No SQL query found in the response.")
            return ''

# @app.callback(
#     [Output('sql-output', 'children'),
#      Output('query-result', 'children')],
#     Input('convert-button', 'n_clicks'),
#     [Input('user-input', 'value')]
# )
def update_output_2(n_clicks, user_input):
    if n_clicks > 0 and user_input:
        sql_query = return_sql_statment(user_input)
        sql_query = sql_query.replace("\n", " ").strip()
        print(sql_query)
        sql_query = sql_query.rstrip(';')  # Remove semicolon if it's there
        sql_output = f"Generated SQL Query:\n{sql_query}"
        engine = get_db_connection()
        with engine.connect() as conn:
            try:
                query_result = conn.execute(text(sql_query))
                records = query_result.fetchall()
                print(records)
                if records:
                    columns = ['Event_Name', 'County', 'Address', 'Latitude', 'Longitude', 'Event_Type', 'Population_Served', 'Number_Trained', 'Hours', 'Date', 'Demographic_Information', 'Identified_Gaps']
                    df = pd.DataFrame(records, columns=columns)
                    query_result_output = html.Div(dash_table.DataTable(
                            id='uploaded-table',
                            columns=[{"name": col, "id": col} for col in df.columns],
                            data=df.to_dict('records'),
                            page_size=10,  
                            style_table={
                            'width': '100%',  
                            'overflowX': 'auto',  
                            'maxHeight': '400px',  
                            'marginTop': '20px'  
                            },
                            style_cell={
                                'textAlign': 'center',
                                'padding': '10px',
                                'fontSize': '14px',
                                'color': 'darkgreen'
                            },
                            style_header={
                                'backgroundColor': '#f4f4f4',  
                                'fontWeight': 'bold',  
                                'textAlign': 'center' 
                            },
                            style_data={
                                'whiteSpace': 'normal',  
                                'overflow': 'hidden' 
                            },
                            style_data_conditional=[
                                            {
                                                'if': {
                                                    'row_index': 'odd'
                                                },
                                                'backgroundColor': '#f1f1f1'
                                            }
                                        ],
                        ),style={
                                        'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                                        'borderRadius': '10px',
                                        'padding': '10px',
                                        'backgroundColor': 'white',
                                        'margin': '20px auto',
                                        'width': '100%',
                                    },
                        )
            except Exception as e:
                query_result_output = f"Error executing query: {str(e)}"
            return sql_output, query_result_output
        
    return '', ''


if __name__ == '__main__':
    app.run_server(debug=True)
