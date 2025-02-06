import os
import dash
import openai
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.io as pio
from plotly.subplots import make_subplots
import cx_Oracle
from dash import dcc, html, dash_table
from sqlalchemy import create_engine

openai.api_key = "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"

def generate_statistical_summary(data_description):
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant that generates statistical summaries."},
            {"role": "user", "content": f"explain the data for report generation: {data_description}"}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=messages,
            max_tokens=200,  
            temperature=1.0,
        )
        
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Unable to generate summary"

# def create_connection():
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


def fetch_data_from_oracle():
    conn = get_db_connection()
    if conn is None:
        print("Connection to the database failed!")
        return []
    try:
        query = "SELECT * FROM dataoutput"  
        df = pd.read_sql(query, conn)
        df.columns = df.columns.str.strip()
        print("Columns after stripping spaces:", df.columns)       
  
        df.columns = df.columns.str.strip()
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']
        df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)        
        return df
    except Exception as e:
        print(f"Error executing query: {e}")
        return pd.DataFrame()  # Return empty DataFrame
    finally:
        conn.dispose()  # Close the connection

# Ensure this folder exists
output_folder = "images"
os.makedirs(output_folder, exist_ok=True)

def create_advanced_visualizations(df):
    def create_violin_plot(df):
        fig = go.Figure()
        
        for sector in df['Sector'].unique():
            sector_data = df[df['Sector'] == sector]['num_participants']
            fig.add_trace(go.Violin(
                x=[sector] * len(sector_data),
                y=sector_data,
                name=sector,
                box_visible=True,
                meanline_visible=True
            ))
        
        fig.update_layout(
            title='Distribution of Participants Across Sectors',
            xaxis_title='Sector',
            yaxis_title='Number of Participants',
            violingap=0,
            violinmode='overlay'
        )
        fig.update_layout(
            plot_bgcolor='white', 
            paper_bgcolor='white',
            title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
            title_x=0,
            title_y=1,
            margin=dict(l=50, r=50, t=50, b=50),
            xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
            yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold')
        )
        
        # Save image and generate summary (optional)
        image_path = os.path.join(output_folder, "output_violin.png")
        pio.write_image(fig, image_path)
        
        return fig

    def create_heatmap(df):
        heatmap_data = df.pivot_table(
            index='Year', 
            columns='Month', 
            values='num_participants', 
            aggfunc='sum'
        )
        
        fig = px.imshow(
            heatmap_data, 
            labels=dict(x="Month", y="Year", color="Participants"),
            title="Participants Heatmap by Year and Month"
        )
        fig.update_layout(
            plot_bgcolor='white', 
            paper_bgcolor='white',
            title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
            title_x=0,
            title_y=1,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        # Save image
        image_path = os.path.join(output_folder, "output_heatmap.png")
        pio.write_image(fig, image_path)
        
        return fig

    def create_boxplot(df):
        fig = go.Figure()
        
        for sector in df['Sector'].unique():
            sector_data = df[df['Sector'] == sector]['num_participants']
            fig.add_trace(go.Box(
                y=sector_data,
                name=sector,
                boxpoints='outliers' 
            ))
        
        fig.update_layout(
            title='Boxplot of Participants by Sector',
            yaxis_title='Number of Participants'
        )
        fig.update_layout(
            plot_bgcolor='white', 
            paper_bgcolor='white',
            title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
            title_x=0,
            title_y=1,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        # Save image
        image_path = os.path.join(output_folder, "output_boxplot.png")
        pio.write_image(fig, image_path)
        
        return fig

    def create_bubble_chart(df):
        bubble_data = df.groupby(['Year', 'Sector'])['num_participants'].sum().reset_index()
        
        fig = px.scatter(
            bubble_data, 
            x='Year', 
            y='num_participants', 
            size='num_participants',
            color='Sector',
            hover_name='Sector',
            title='Bubble Chart of Participants by Year and Sector'
        )
        fig.update_layout(
            plot_bgcolor='white', 
            paper_bgcolor='white',
            title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
            title_x=0,
            title_y=1,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        # Save image
        image_path = os.path.join(output_folder, "output_bubble.png")
        pio.write_image(fig, image_path)
        
        return fig

    # Create visualizations
    visualizations = [
        create_violin_plot(df),
        create_heatmap(df),
        create_boxplot(df),
        create_bubble_chart(df)
    ]

    # Create graph elements with unique IDs
    graph_elements = [
        dcc.Graph(id=f'graph-{i}', figure=fig) 
        for i, fig in enumerate(visualizations)
    ]
    
    return graph_elements

def update_graph_db():
    # Fetch data and create visualizations
    df = fetch_data_from_oracle()
    
    # Ensure column names are stripped
    df.columns = df.columns.str.strip()
    
    # Create graph elements
    graph_elements = create_advanced_visualizations(df)
    
    return graph_elements

# Initialize Dash app
app = dash.Dash(__name__)

# Create app layout
def create_app_layout():
    return html.Div([
        html.H1("Participant Data Visualization", 
                style={
                    'textAlign': 'center', 
                    'color': 'darkgreen', 
                    'marginBottom': '20px'
                }),
        
        html.Div([
            html.H3(
                "Visualization of Participants Across Different Sectors", 
                style={
                    'textAlign': 'left', 
                    'marginLeft': '50px', 
                    'color': 'darkgreen'
                }
            ),
            
            # Add the graphs
            html.Div(
                update_graph_db(),
                style={'margin': '20px'}
            )
        ])
    ])

# def test_sector_graph(): 
#       return create_app_layout()

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)