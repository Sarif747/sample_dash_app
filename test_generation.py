import html
import os
import openai

# openai.api_key = "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"

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import cx_Oracle

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

def fetch_data_from_oracle():
    conn = create_connection()
    if conn is None:
        print("Connection to the database failed!")
        return []
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM participants_data"  
        cursor.execute(query)     
        rows = cursor.fetchall()        
        columns = [desc[0] for desc in cursor.description]       
        df = pd.DataFrame(rows, columns=columns)
        df.columns = df.columns.str.strip()
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']
        df['MONTH'] = pd.Categorical(df['MONTH'], categories=month_order, ordered=True)        
        return df
    except cx_Oracle.Error as e:
        print(f"Error executing query: {e}")
        return pd.DataFrame()
    finally:
        cursor.close()
        conn.close()
output_folder = "images"

def create_advanced_visualizations(df):
    graph_elements = []
    
    # 1. Heatmap of Participants by Sector and Month
    plt.figure(figsize=(12, 8))
    heatmap_data = df.pivot_table(
        index='SECTOR', 
        columns='MONTH', 
        values='NUM_PARTICIPANTS', 
        aggfunc='sum'
    )
    
    plt.figure(figsize=(15, 10))
    sns.heatmap(heatmap_data, annot=True, cmap='YlGnBu', fmt='.0f')
    plt.title('Participants Heatmap by Sector and Month', fontsize=16)
    plt.tight_layout()
    heatmap_path = os.path.join(output_folder, 'heatmap.png')
    plt.savefig(heatmap_path)
    plt.close()

    # 2. Violin Plot for Participant Distribution
    plt.figure(figsize=(12, 8))
    sns.violinplot(x='SECTOR', y='NUM_PARTICIPANTS', data=df)
    plt.title('Participant Distribution by Sector', fontsize=16)
    plt.xticks(rotation=45)
    violin_path = os.path.join(output_folder, 'violin_plot.png')
    plt.savefig(violin_path)
    plt.close()

    # 3. Advanced Plotly Sunburst Chart
    sunburst_df = df.groupby(['YEAR', 'SECTOR', 'MONTH'])['NUM_PARTICIPANTS'].sum().reset_index()
    fig_sunburst = px.sunburst(
        sunburst_df, 
        path=['YEAR', 'SECTOR', 'MONTH'], 
        values='NUM_PARTICIPANTS',
        title='Hierarchical View of Participants'
    )
    sunburst_path = os.path.join(output_folder, 'sunburst_chart.png')
    fig_sunburst.write_image(sunburst_path)

    # 4. Box Plot with Swarm Plot Overlay
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='SECTOR', y='NUM_PARTICIPANTS', data=df)
    sns.swarmplot(x='SECTOR', y='NUM_PARTICIPANTS', data=df, color=".25")
    plt.title('Participant Distribution with Outliers', fontsize=16)
    plt.xticks(rotation=45)
    boxplot_path = os.path.join(output_folder, 'boxplot.png')
    plt.savefig(boxplot_path)
    plt.close()

    # 5. Advanced Time Series with Confidence Interval
    plt.figure(figsize=(15, 10))
    sns.lineplot(
        x='MONTH', 
        y='NUM_PARTICIPANTS', 
        hue='SECTOR', 
        data=df, 
        ci=68  # 68% confidence interval
    )
    plt.title('Monthly Participants Trend by Sector', fontsize=16)
    plt.xticks(rotation=45)
    timeseries_path = os.path.join(output_folder, 'time_series.png')
    plt.savefig(timeseries_path)
    plt.close()

    # 6. Plotly Parallel Coordinates Plot
    parallel_df = df.groupby(['SECTOR', 'YEAR', 'MONTH'])['NUM_PARTICIPANTS'].sum().reset_index()
    fig_parallel = px.parallel_coordinates(
        parallel_df, 
        color='NUM_PARTICIPANTS',
        dimensions=['YEAR', 'MONTH', 'NUM_PARTICIPANTS'],
        color_continuous_scale=px.colors.sequential.Viridis,
        title='Parallel Coordinates of Participants'
    )
    parallel_path = os.path.join(output_folder, 'parallel_coordinates.png')
    fig_parallel.write_image(parallel_path)

    # Convert images to Dash graph elements
    graph_paths = [
        heatmap_path, violin_path, sunburst_path, 
        boxplot_path, timeseries_path, parallel_path
    ]
    
    for path in graph_paths:
        graph_elements.append(html.Img(src=path, style={'width': '100%', 'max-width': '800px'}))

    return graph_elements

def update_graph_db():
    df = fetch_data_from_oracle()
    df.columns = df.columns.str.strip()
    
    # Preprocess data if needed
    df['MONTH'] = pd.Categorical(df['MONTH'], 
        categories=['January', 'February', 'March', 'April', 'May', 'June', 
                    'July', 'August', 'September', 'October', 'November', 'December'],
        ordered=True
    )
    
    return create_advanced_visualizations(df)

if __name__ == '__main__':
        update_graph_db()