import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import openai
import pandas as pd
from sqlalchemy import create_engine, text
import re
import dash_bootstrap_components as dbc
import plotly.express as px
from dotenv import load_dotenv
import os


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


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Enter your query",style={'textAlign': 'left', 'marginLeft': '20px', 'color': 'darkgreen'}),
    dbc.Row([
        dcc.Textarea(
            id='user-input',
            style={'width': '100%', 'height': 100},
            placeholder="Enter your query here, e.g., 'Show me all users with age greater than 30'",
    ),]),
    dbc.Button('submit', id='convert-button', n_clicks=0,style={"margin-top": "40px",'color': 'white',"backgroundColor": "darkgreen"}),
    html.Div(id='sql-output', style={'white-space': 'pre-wrap', 'marginTop': '20px'}),
    html.Div(id='query-result', style={'marginTop': '20px'}),
    html.Div(id='graph-output', style={'marginTop': '20px'}),

],style={
                            'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                            'borderRadius': '10px',
                            'padding': '10px',
                            'backgroundColor': 'white',
                            'margin': '20px auto',
                            'width': '95%',
                        })


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
# Function to generate the graph code using GPT
def generate_graph_code(description):
    messages = [
        {"role": "system", "content": "You are a helpful assistant that generates code for statistical graphs using Python and Plotly."},
        {"role": "user", "content": f"Generate Python code to create a graph based on this description: {description}"}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=messages,
        max_tokens=500,
        temperature=0.7,
    )
    graph_code = response['choices'][0]['message']['content'].strip()
    print(graph_code)
    return graph_code

@app.callback(
    [Output('sql-output', 'children'),
     Output('query-result', 'children'),
     Output('graph-output','children')],
    Input('convert-button', 'n_clicks'),
    [Input('user-input', 'value')]
)
def update_output(n_clicks, user_input):
    if n_clicks > 0 and user_input:
        sql_query = return_sql_statment(user_input)
        sql_output = f"Generated SQL Query:\n{sql_query}"
        engine = get_db_connection()
        try:
            with engine.connect() as conn:
                query_result = conn.execute(text(sql_query))
                records = query_result.fetchall()
                if records:
                    columns = ["event_name", "county", "address", "latitude", "longitude",
                        "event_type", "population_served", "number_trained", "hours",
                        "event_date", "demographic_info", "identified_gaps"]
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
                                        'width': '95%',
                                    },
                        ),
                        # Generate a bar plot or any statistical graph (e.g., histogram, line chart, etc.)
                    df = pd.DataFrame(records, columns=columns)

                    # Now generate the graph using GPT
                    graph_code = generate_graph_code(df)
                    
                    # The generated graph code will need to be evaluated and executed.
                    # You can use Python's `exec` function to evaluate the generated code, but be cautious of security risks in a production environment.
                    # exec(graph_code)  # Make sure to sanitize inputs in real applications for security
                    print(graph_code)
                    # Return the graph
                    return sql_query,query_result_output,graph_code
        except Exception as e:
            query_result_output = f"Error executing query: {str(e)}"
        
        return sql_output, query_result_output,''
    return '', '',''

if __name__ == '__main__':
    app.run_server(debug=True)