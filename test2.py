import seaborn as sns
import matplotlib.pyplot as plt
import plotly.tools as tls
import plotly.graph_objs as go
import plotly.express as px
import dash
import pandas as pd
import cx_Oracle
from dash import dcc, html
from sqlalchemy import create_engine


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

# # Database connection
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

def fetch_data_from_oracle():
    conn = get_db_connection()
    if conn is None:
        print("Connection to the database failed!")
        return pd.DataFrame()  # Return empty DataFrame
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM dataoutput"  
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        df.columns = df.columns.str.strip()  # Clean column names
        # Ordering months
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                       'July', 'August', 'September', 'October', 'November', 'December']
        df['MONTH'] = pd.Categorical(df['MONTH'], categories=month_order, ordered=True)
        return df
    except cx_Oracle.Error as e:
        print(f"Error executing query: {e}")
        return pd.DataFrame()  # Return empty DataFrame
    finally:
        cursor.close()
        conn.close()

def fetch_data_from_azure():
    conn = get_db_connection()
    if conn is None:
        print("Connection to the database failed!")
        return pd.DataFrame()  # Return empty DataFrame
    
    try:
        # Use pandas to read SQL directly
        query = "SELECT * FROM dataoutput"
        df = pd.read_sql(query, conn)
        df.columns = df.columns.str.strip()

# Check again after stripping spaces
        print("Columns after stripping spaces:", df.columns)
        # Clean column names
        # df.columns = df.columns.str.strip()
        
        # Ordering months
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                       'July', 'August', 'September', 'October', 'November', 'December']
        df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)
        
        return df
    except Exception as e:
        print(f"Error executing query: {e}")
        return pd.DataFrame()  # Return empty DataFrame
    finally:
        conn.dispose()  # Close the connection


# Convert Seaborn figure to Plotly
def seaborn_to_plotly(seaborn_fig):
    return tls.mpl_to_plotly(seaborn_fig)

# Create Seaborn visualizations with Plotly conversion
def create_seaborn_visualizations(df):
    if df.empty:
        return [html.Div("No data available.")]

    graph_elements = []

    def create_advanced_seaborn_plots():
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))

        # Violin Plot
        sns.violinplot(x='Sector', y='num_participants', data=df, ax=axes[0, 0])
        axes[0, 0].set_title('Violin Plot of Participants by Sector')

        # Swarm Plot
        sns.swarmplot(x='Sector', y='num_participants', data=df, ax=axes[0, 1])
        axes[0, 1].set_title('Swarm Plot of Participants')

        # Box Plot
        sns.boxplot(x='Sector', y='num_participants', data=df, ax=axes[1, 0])
        axes[1, 0].set_title('Box Plot of Participants')

        # Scatter Plot
        sns.scatterplot(x='Year', y='num_participants', data=df, ax=axes[1, 1])
        axes[1, 1].set_title('Scatter Plot of Participants')

        plt.tight_layout()

        # Convert to Plotly
        plotly_fig = seaborn_to_plotly(fig)
        plt.close(fig)

        return plotly_fig

    def create_interactive_seaborn_plot():
        # Clean the 'SECTOR' column to handle any 'None' or invalid values
         df_clean = df.dropna(subset=['Sector'])
         return px.box(df_clean, x='Sector', y='num_participants', color='Sector', points='all', title='Interactive Box Plot of Participants')

    def create_statistical_visualization():
        return px.scatter_matrix(df, dimensions=['Year', 'num_participants'], title='Scatter Matrix of Participants')

    def create_joint_distribution():
        fig = go.Figure()
        fig.add_trace(go.Histogram2d(x=df['Year'], y=df['num_participants']))
        fig.add_trace(go.Histogram(x=df['Year'], yaxis='y2', opacity=0.5))
        fig.add_trace(go.Histogram(y=df['num_participants'], xaxis='x2', opacity=0.5))
        fig.update_layout(
            title='Joint Distribution of Year and Participants',
            xaxis2=dict(title='Year', overlaying='x', side='top'),
            yaxis2=dict(title='Participants', overlaying='y', side='right')
        )
        return fig

    # Collect visualizations
    visualizations = [
        create_advanced_seaborn_plots(),
        create_interactive_seaborn_plot(),
        create_statistical_visualization(),
        create_joint_distribution()
    ]

    # Convert to Dash graph elements
    graph_elements = [dcc.Graph(figure=fig) for fig in visualizations]

    return graph_elements

def update_graph_db():
    df = fetch_data_from_azure()
    df['Sector'] = df['Sector'].astype(str)  # Convert to string, if necessary
    return create_seaborn_visualizations(df)

# Dash app setup
app = dash.Dash(__name__)

app.layout = html.Div(update_graph_db())  # Place all visualizations in a div

if __name__ == '__main__':
    app.run_server(debug=True)
