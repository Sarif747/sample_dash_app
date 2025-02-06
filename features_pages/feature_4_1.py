import dash
from dash import dcc, html
from dash import dash_table
from flask import send_from_directory
import pandas as pd
import random
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import cx_Oracle
import os
import plotly.io as pio
from sqlalchemy import create_engine, text
from transformers import pipeline
import openai
from dotenv import load_dotenv
import os

summarizer = pipeline("text2text-generation", model="facebook/bart-large-cnn")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(OPENAI_API_KEY)

openai.api.key = OPENAI_API_KEY
# openai.api_key = "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"

def generate_statistical_summary(data_description):
    # prompt = f"Generate a statistical summary based on the following data: {data_description}"
    messages = [
        {"role": "system", "content": "You are a helpful assistant that generates statistical summaries."},
        {"role": "user", "content": f"explain the data for report generation: {data_description}"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=messages,
        max_tokens=300,  
        temperature=1.0,  # Control the creativity of the model (0.0 = deterministic, 1.0 = creative)
    )
    
    return response['choices'][0]['message']['content'].strip()


OUTPUT_DIR = os.getcwd()

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

def create_connection():
    try:
        connection = cx_Oracle.connect(
            user='system',    
            password='orcl', 
            dsn='localhost:1521/orcl'           
        )
        print("Connection successful!")
        return connection
    except cx_Oracle.Error as e:
        error, = e.args
        print(f"Error connecting to Oracle: {error.code}, {error.message}")
        return None

def fetch_data_from_oracle_1():
    conn = get_db_connection()
    if conn is None:
        print("Connection to the database failed!")
        return []
    try:
        query = "SELECT * FROM event_data"  
        df = pd.read_sql(query, conn)
        df.columns = df.columns.str.strip()

# Check again after stripping spaces
        print("Columns after stripping spaces:", df.columns)
        
        return df
    except Exception as e:
        print(f"Error executing query: {e}")
        return pd.DataFrame()  # Return empty DataFrame
    finally:
        conn.dispose()  # Close the connection


df = fetch_data_from_oracle_1()
df.columns = df.columns.str.strip()
app = dash.Dash(__name__)

def download_file(filename):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(file_path):
        return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)
    else:
        return "File not found.", 404
    
output_folder = "images"

def testing_page_4():
    df = fetch_data_from_oracle_1()
    df.columns = df.columns.str.strip()
    html.Div(
    style={'backgroundColor': '#f0f4e1', 'padding': '20px'},
    children=[
        html.H1(
            "Impact Metrix  Dashboard",
            style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}
        ),
        html.Div(
                style={
                        'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                        'borderRadius': '10px',
                        'padding': '10px',
                        'backgroundColor': 'white',
                        'margin': '20px auto',
                    },            
                children=[
                html.Label("Select Counties:", style={'fontSize': '18px', 'color': 'darkgreen'}),
                dcc.Dropdown(
                    id='county-dropdown',
                    options=[{'label': Location, 'value': Location} for Location in df['Location'].unique()],
                    value=['Colquitt'],  
                    multi=True,  
                    style={'width': '100%', 'padding': '10px'}
                ),
            ] 
        ),
        html.Div(
                style={
                        'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                        'borderRadius': '10px',
                        'padding': '10px',
                        'backgroundColor': 'white',
                        'margin': '20px auto',
                    },            
                children=[
                html.Label("Data Table for Selected Counties:", style={'fontSize': '18px', 'color': 'darkgreen'}),
                dash_table.DataTable(
            id='data-table',
            page_size=10,  
            sort_action="native",  
            filter_action="native", 
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
        )
            ]
        ),

        dbc.Row([
        dbc.Col(
            html.Div(
                style={
                    'display': 'flex',
                    'justifyContent': 'space-between',  
                    'gap': '20px',  
                    'flex': 1, 
                    'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                    'borderRadius': '10px',
                    'padding': '10px',
                    'backgroundColor': 'white',
                    'margin': '20px auto',
                },
                children=[
                    dcc.Graph(
                        id='training-type-bar',
                        style={'flex': 1, 'height': '400px', 'margin': 'auto'}  
                    ),
                    dcc.Graph(
                        id='knowledge-percent-box',
                        style={'flex': 1, 'height': '400px', 'margin': 'auto'}
                    ),
                ]
            ),
            width=12  
        ),
    ]),

    dbc.Row([
        dbc.Col(
            html.Div(
                style={
                    'display': 'flex',
                    'justifyContent': 'space-between',
                    'gap': '20px',  
                    'flex': 1,  
                    'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                    'borderRadius': '10px',
                    'padding': '10px',
                    'backgroundColor': 'white',
                    'margin': '20px auto',
                },
                children=[
                    dcc.Graph(
                        id='duration-distribution',
                        style={'flex': 1, 'height': '400px', 'margin': 'auto'}
                    ),
                    dcc.Graph(
                        id='correlation-heatmap',
                        style={'flex': 1, 'height': '400px', 'margin': 'auto'}
                    ),
                ]
            ),
            width=12  
        ),
        ]),
    ]
)
summaries = []
# @app.callback(
#     Output('data-table', 'data'),
#     Output('data-table', 'columns'),
#     Input('county-dropdown', 'value')
# )
def display_table(selected_counties):
    filtered_df = df[df['Location'].isin(selected_counties)]
    columns = [{'name': col, 'id': col} for col in filtered_df.columns]
    return filtered_df.to_dict('records'), columns

# @app.callback(
#     Output('training-type-bar', 'figure'),
#     Input('county-dropdown', 'value')
# )
def update_training_type_bar(selected_counties):
    if isinstance(selected_counties, str):
        selected_counties = [selected_counties]
    filtered_df = df[df['Location'].isin(selected_counties)]

    fig = px.histogram(filtered_df, x='Training_Type_if_applicable', color='Training_Type_if_applicable', 
                       title=f"Training Types in {', '.join(selected_counties)}")
    summary_1 = generate_statistical_summary(fig)
    print("Generated Summary:", summary_1)
    # summaries.append(summary_1)
    with open('summary_1.txt', 'w') as file:
            file.write(summary_1 + "\n\n")
    print("Summaries have been written to summaries.txt.")
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))
    image_path = os.path.join(output_folder, f"output_update_training_type.png")
    pio.write_image(fig, image_path)
    return fig

# @app.callback(
#     Output('knowledge-percent-box', 'figure'),
#     Input('county-dropdown', 'value')
# )
def update_knowledge_percent_box(selected_counties):
    if isinstance(selected_counties, str):
        selected_counties = [selected_counties]
    filtered_df = df[df['Location'].isin(selected_counties)]
    fig = px.box(filtered_df, y='Percent_of_participants_with_increased_knowledge_skills_and_or_abilities', 
                 title=f"Percent of Participants with Increased Knowledge in {', '.join(selected_counties)}")
    summary_2 = generate_statistical_summary(fig)
    print("Generated Summary:", summary_2)
    # summaries.append(summary_2)
    with open('summary_2.txt', 'w') as file:
            file.write(summary_2 + "\n\n")
    print("Summaries have been written to summaries.txt.")
    fig.update_layout(
        yaxis_title='Knowledge Increase'  
    )
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))
    image_path = os.path.join(output_folder, f"output_update_knowledge_percent_box.png")
    pio.write_image(fig, image_path)
    return fig

# @app.callback(
#     Output('duration-distribution', 'figure'),
#     Input('county-dropdown', 'value')
# )
def update_duration_distribution(selected_counties):
    if isinstance(selected_counties, str):
        selected_counties = [selected_counties]
    filtered_df = df[df['Location'].isin(selected_counties)]
    filtered_df.loc[:, 'Duration_Hours'] = pd.to_numeric(filtered_df['Duration_Hours'], errors='coerce')
    filtered_df = filtered_df.dropna(subset=['Duration_Hours'])
   
    fig = px.histogram(filtered_df, x='Duration_Hours', 
                       title=f"Training Duration Distribution in {', '.join(selected_counties)}")
    summary_3 = generate_statistical_summary(fig)
    print("Generated Summary:", summary_3)
    # summaries.append(summary_3)
    with open('summary_3.txt', 'w') as file:
            file.write(summary_3 + "\n\n")
    print("Summaries have been written to summaries.txt.")
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))
    image_path = os.path.join(output_folder, f"output_update_duration_distribution.png")
    pio.write_image(fig, image_path)
    return fig

# @app.callback(
#     Output('correlation-heatmap', 'figure'),
#     Input('county-dropdown', 'value')
# )
def update_correlation_heatmap(selected_counties):
    if isinstance(selected_counties, str):
        selected_counties = [selected_counties]  
    filtered_df = df[df['Location'].isin(selected_counties)]
    if filtered_df.empty:
        return {}  
    corr_df = filtered_df[['Total_Participants', 'Total_Registrants', 'Training_or_Event_Capacity']].corr()
    corr_str = corr_df.to_string()

    # summary = summarizer(corr_str, max_length=200, min_length=50, do_sample=False)
    # print(summary)
    data_description = """
        Total Participants  Total Registrants  Training or Event CapacityTotal Participants 1.000000 1.550534 1.379184 0.098507 0.000000 -0.9881 0.9761 1.56600 1.66400 1,664,000 1.764,500 1.865,000 2.564,200 1.972,000.
    """
    summary_4 = generate_statistical_summary(corr_df)
    print("Generated Summary:", summary_4)
    print(summaries)
    # summaries.append(summary_4)
    with open('summary_4.txt', 'w') as file:
            file.write(summary_4 + "\n\n")
    print("Summaries have been written to summaries.txt.")
    fig = px.imshow(corr_df, text_auto=True, 
                    title=f"Correlation Heatmap in {', '.join(selected_counties)}")
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))
    image_path = os.path.join(output_folder, f"output_update_duration_distribution.png")
    pio.write_image(fig, image_path)
    image_path = os.path.join(output_folder, f"output_update_correlation_heatmap.png")
    pio.write_image(fig, image_path)
    return fig

# print(summaries)
# try:
#     with open('summaries.txt', 'w') as file:
#         for summary in summaries:
#             file.write(summary + "\n\n")
#     print("Summaries have been written to summaries.txt.")
# except Exception as e:
#     print(f"An error occurred: {e}")


if __name__ == '__main__':
    app.run_server(debug=True)
