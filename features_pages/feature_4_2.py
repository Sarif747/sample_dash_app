import base64
import subprocess
import time
import cx_Oracle
from flask import app, send_file, send_from_directory
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash import dash_table
import plotly.express as px
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.io as pio
import os
from sqlalchemy import create_engine, text
from test_graph import create_app_layout

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True,prevent_initial_callbacks='initial_duplicate')
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
  
def add_data_to_oracle(sector, year, month, num_participants):
    engine = get_db_connection()
    if engine is None:
        return "Failed to connect to the database"
    with engine.connect() as conn:
        try:
            insert_query = text("""INSERT INTO dataoutput (Sector, Year, Month, num_participants) 
                            VALUES (:sector, :year, :month, :num_participants)""")
            conn.execute(insert_query, {'sector': sector, 'year': year, 'month': month, 'num_participants': num_participants})
            conn.commit()
            return "Data added successfully"
        except cx_Oracle.Error as e:
            print(f"Error inserting data: {e}")
            return "Failed to add data"
        finally:
            conn.close()
            conn.close()

def update_data_in_oracle(sector, year, month, num_participants):
    engine = get_db_connection()
    if conn is None:
        return "Failed to connect to the database"
    with engine.connect() as conn:
        try:
            update_query = text("""UPDATE dataoutput
                            SET num_participants = :num_participants
                            WHERE Sector = :sector AND Year = :year AND Month = :month""")
            conn.execute(update_query, {'sector': sector, 'year': year, 'month': month, 'num_participants': num_participants})
            conn.commit()
            print('arif')
            return "Data updated successfully"
        except cx_Oracle.Error as e:
            print(f"Error updating data: {e}")
            return "Failed to update data"
        finally:
            conn.close()
            conn.close()

def check_existing_data(sector, month, year):
    engine = get_db_connection()
    if conn is None:
        return "Failed to connect to the database"
    with engine.connect() as conn:
        try:
            query = text("""
            SELECT * FROM dataoutput WHERE SECTOR = :sector AND MONTH = :month AND YEAR = :year
            """)
            result = conn.execute(query, {'sector': sector, 'year': year, 'month': month})
            conn.commit()
            result = conn.fetchall()
            print(result)
            if result:  
                print("adeeb")
                return "Data already exists for this Sector, Month, and Year"
            else:
                return None       
        except cx_Oracle.Error as e:
            print(f"Error updating data: {e}")
            return "Failed to check data"
        finally:
            conn.close()
            conn.close()

def delete_record(sector, month, year,num_participants):
    engine = get_db_connection()
    if conn is None:
        return "Failed to connect to the database"   
    with engine.connect() as conn:
        try:
            query = text("""
            DELETE FROM dataoutput
            WHERE SECTOR = :sector AND MONTH = :month AND YEAR = :year AND NUM_PARTICIPANTS = :num_participants
            """)
            conn.execute(query, {'sector': sector, 'month': month, 'year': year, 'num_participants': num_participants})
            conn.commit()
            return "Record deleted successfully"
        except cx_Oracle.Error as e:
            print(f"Error deleting record: {e}")
            return "Failed to delete record"
        finally:
            conn.close()
            conn.close()


df = fetch_data_from_oracle()
OUTPUT_DIR = os.getcwd()
output_pdf = os.path.join(OUTPUT_DIR, "quarto.pdf"),

# app.layout = 
def CURD_Operation():
    return html.Div([
                html.H1("Participants Data in each sector",style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
                html.H5("This section shows the interactive statistical visualization of participants in each sectors over the years",style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
                dbc.Row([
                    dbc.Col([
                        html.Div(
                            style={
                                'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                                'borderRadius': '10px',
                                'padding': '10px',
                                'backgroundColor': 'white',
                                'margin': '20px auto',
                                'width': '100%',
                            },                   
                            children=[
                                # html.Div(id='graphs-container', style={'display': 'flex', 'flex-wrap': 'wrap'}),
                                create_app_layout()
                            ]
                        )
                        ],width=12),
                dbc.Row([
                    html.H3("Search number of participants by secotor, year and month",style={'textAlign': 'left', 'marginLeft': '20px', 'color': 'darkgreen'}),
                    html.H5("User can serach for number of participants and  their details by selecting the sector, year and month from the dropdown options below",style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
                    dbc.Col([
                        html.Div([
                                html.H5("Sector",style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
                                dbc.Col([
                                    dcc.Dropdown(id='search-sector-dropdown', options=[], value='',style={
                                        'width': '300px',
                                        'height': '40px',
                                        'marginLeft': '25px',
                                        'textAlign': 'center',
                                        'color': 'darkgreen',
                                        }),
                                ],width=4),
                                html.H5("Year",style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
                                dbc.Col([
                                    dcc.Dropdown(id='search-year-dropdown', options=[], value='',style={
                                    'width': '300px',
                                    'height': '40px',
                                    'marginLeft': '25px',
                                    'textAlign': 'center',
                                    'color': 'darkgreen',
                                    }),
                                ],width=4),
                                html.H5("Month",style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
                                dbc.Col([
                                    dcc.Dropdown(id='search-month-dropdown', options=[], value='',style={
                                    'width': '300px',
                                    'height': '40px',
                                    'marginLeft': '25px',
                                    'textAlign': 'center',
                                    'color': 'darkgreen',
                                })
                                ],width=4),    
                        ]),
                    ],style={'textAlign': 'left', 'marginLeft': '10px'}),
                    dbc.Col([
                        html.H5("Search Results",style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
                        html.Div(
                                style={
                                'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                                'padding': '10px',
                                'backgroundColor': 'white',
                                'margin': '20px auto',
                                'width': '1100px',
                            },children=[
                            dash_table.DataTable(
                                    id='search-results-table',
                                    columns=[
                                        {'name': 'SECTOR', 'id': 'SECTOR'},
                                        {'name': 'MONTH', 'id': 'MONTH'},
                                        {'name': 'YEAR', 'id': 'YEAR'},
                                        {'name': 'NUM_PARTICIPANTS', 'id': 'NUM_PARTICIPANTS'},
                                    ],
                                    editable=True,
                                    row_deletable=True,
                                    style_table={'overflowX': 'auto'},
                                    style_cell={
                                        'textAlign': 'center',
                                        'padding': '10px',
                                        'fontSize': '14px',
                                        'backgroundColor': '#f9f9f9'
                                    },
                                    style_header={
                                        'backgroundColor': 'darkgreen',
                                        'color': 'white',
                                        'fontWeight': 'bold',
                                        'textAlign': 'center'
                                    },
                                    style_data={
                                        'backgroundColor': 'white',
                                        'color': 'black'
                                    },
                                    style_data_conditional=[
                                        {
                                            'if': {
                                                'row_index': 'odd'
                                            },
                                            'backgroundColor': '#f1f1f1'
                                        }
                                    ],
                                ),
                        ]),  
                    ]),
                    ]),
                ]),
                dbc.Row([
                    # dbc.Col([
                    #     html.H3("Add Data",style={'textAlign': 'left', 'marginLeft': '20px', 'color': 'darkgreen'}),
                    #     html.Div([
                    #         html.Label("Sector",style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
                    #         dcc.Input(id='add-sector-input', type='text', placeholder='Enter sector', value='',style={
                    #                 'width': '200px',
                    #                 'height': '40px',
                    #                 'textAlign': 'center',
                    #                 'color': 'darkgreen',
                    #             }),
                    #         html.Label("Year",style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
                    #         dcc.Input(id='add-year-input', type='number', placeholder='Enter year', value=2020,style={
                    #                 'width': '200px',
                    #                 'height': '40px',
                    #                 'textAlign': 'center',
                    #                 'color': 'darkgreen',
                    #             }),
                    #         html.Label("Month",style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
                    #         dcc.Input(id='add-month-input', type='text', placeholder='Enter month', value='January',style={
                    #                 'width': '200px',
                    #                 'height': '40px',
                    #                 'textAlign': 'center',
                    #                 'color': 'darkgreen',
                    #             }),
                    #         html.Label("Number of Participants",style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
                    #         dcc.Input(id='add-participants-input', type='number', value=1,style={
                    #                 'width': '200px',
                    #                 'height': '40px',
                    #                 'textAlign': 'center',
                    #                 'color': 'darkgreen',
                    #             }),
                    #         dbc.Button("Add Data", id='add-button', n_clicks=0,style={
                    #                 'width': '200px',
                    #                 'height': '40px',
                    #                 'textAlign': 'center',
                    #                 'color': 'darkgreen',
                    #             }),
                    #         html.Div(id='output_message',style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
                    #     ],style={
                    #         'display': 'flex', 
                    #         'justifyContent': 'space-between',  
                    #         'alignItems': 'center',  
                    #         'gap': '20px',  
                    #     }),                       
                    # ]),
                    html.Br(),
                    dbc.Col([
                        # html.H3("Update Data",style={'textAlign': 'left', 'marginLeft': '20px', 'color': 'darkgreen'}),
                        # html.Div([
                        #     html.Label("Sector",style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
                        #     dcc.Dropdown(
                        #         id='update-sector-dropdown', 
                        #         options=[], 
                        #         style={
                        #             'width': '200px',
                        #             'height': '40px',
                        #             'textAlign': 'center',
                        #             'color': 'darkgreen',
                        #         }
                        #     ),
                        #     html.Label("Year",style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
                        #     dcc.Dropdown(
                        #         id='update-year-dropdown', 
                        #         options=[], 
                        #         style={
                        #             'width': '200px',
                        #             'height': '40px',
                        #             'textAlign': 'center',
                        #             'color': 'darkgreen',
                        #         }
                        #     ),
                        #     html.Label("Month",style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
                        #     dcc.Dropdown(
                        #         id='update-month-dropdown', 
                        #         options=[], 
                        #         style={
                        #             'width': '200px',
                        #             'height': '40px',
                        #             'textAlign': 'center',
                        #             'color': 'darkgreen',
                        #         }
                        #     ),
                        #     html.Label("Number of Participants",style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
                        #     dcc.Input(
                        #         id='update-participants', 
                        #         type='number', 
                        #         value=1,
                        #         style={
                        #             'width': '200px',
                        #             'height': '40px',
                        #             'textAlign': 'center',
                        #             'color': 'darkgreen',
                        #         }
                        #     ),
                        #     html.Button("Update Data", id='update-button',style={
                        #             'width': '200px',
                        #             'height': '40px',
                        #             'textAlign': 'center',
                        #             'color': 'darkgreen',
                        #         }),
                        # ], style={
                        #     'display': 'flex', 
                        #     'justifyContent': 'space-between',  
                        #     'alignItems': 'center',  
                        #     'gap': '20px',  
                        # }),
                        html.Br(),
                        html.Div(id='output_message',style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
                        html.H5("You can generate pdf report of all the visualization by clicking on the generate report button below after few seconds a download report link will appear where you can download your report by clicking on the link",style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
                        dbc.Button("Generate Report", id='download-button_report',n_clicks = 0,style={
                                    'width': '200px',
                                    'height': '40px',
                                    'textAlign': 'center',
                                    'color': 'white',"backgroundColor": "darkgreen"
                                }),
                        # dcc.Store(id='download-link-store'),
                        html.Div(id='download-link-container'), 
                        dcc.Store(id='df-store', data=[])
                    ])                      
                ]),
                
],style={'backgroundColor': 'lightgreen', 'padding': '20px'})

# @app.callback(
#     [Output('download-link-container', 'children'),
#      Output('download-link-store', 'data')],
#     [Input('download-button', 'n_clicks')],
#     [State('download-link-store', 'data')]
# )
def download_report(n_clicks):
    print("report n clicks")
    # print(f"Received n_clicks: {n_clicks}, store_data: {store_data}")
    if n_clicks is None or n_clicks == 0:
        print("PreventUpdate raised")
        children = []
        data = {'download_link': ''}
        return children
    else:
        try:
            print("after clicking the report btton")
            quarto_file = "quarto_text.qmd"  
            output_pdf = os.path.join(OUTPUT_DIR, "quarto_text.pdf")  
            quarto_path = r"C:/Program Files/Quarto/bin/quarto.exe"
            subprocess.run([quarto_path, 'render', quarto_file, '--to', 'pdf'], check=True)
            print("Quarto file rendered successfully.")
            print("after report genration")
            download_link = f"/download/{os.path.basename(output_pdf)}" 
            print('arif')
            if os.path.exists(output_pdf):
                download_link = f"/download/{os.path.basename(output_pdf)}"
                print(f"Output PDF exists: {output_pdf}")
                print(f"Download link: {download_link}")
                return [html.A(
                    'Download Report',
                    href=download_link,
                    download='quarto_text.pdf',
                    target='_blank',
                    style={
                                    'width': '200px',
                                    'height': '40px',
                                    'textAlign': 'center',
                                    'color': 'darkgreen',
                                }
                )]
            else:
                return [html.Div("PDF file not found.", style={'color': 'red'})]
        except subprocess.CalledProcessError as e:
            return [html.Div(f"An error occurred while generating the report: {str(e)}", style={'color': 'red'})]

# @app.server.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(file_path):
        return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)
    else:
        return "File not found.", 404

output_folder = "images"

# @app.callback(
#     Output('graph', 'figure'),
#     [Input('plot-type-dropdown', 'value'),
#      Input('df-store', 'data')]  
# )
def update_graph_db(stored_data):
    df = fetch_data_from_oracle() 
    fig = None
    figures_1 = []
    figures = []
    graph_elements = []
    df.columns = df.columns.str.strip()
    months_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 
                    'September', 'October', 'November', 'December']
    df_grouped = df.groupby(['Year', 'Month', 'Sector'], as_index=False,observed=True)['num_participants'].sum()
    sectors = df['Sector'].unique()
    for sector in sectors:
        sector_df = df_grouped[df_grouped['Sector'] == sector].copy()
        sector_df['Month'] = pd.Categorical(sector_df['Month'], categories=months_order, ordered=True)
        sector_df = sector_df.sort_values('Month')
        fig = px.bar(sector_df, x='YEAR', y='num_participants', color='Month',
                    title=f"Participants in {sector} by Year",
                    labels={'YEAR': 'Year', 'num_participants': 'Number of Participants', 'MONTH': 'Month'},
                    category_orders={'Month': months_order})  
        fig.update_layout(width=500, height=500, showlegend=True)
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
            title_x=0,
            title_y=0.95,
            xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
            yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))
        image_path = os.path.join(output_folder, f"output_{sector.replace(' ', '_').replace('/', '_')}_bar_chart.png")
        pio.write_image(fig, image_path)
        figures.append(fig)
    years = df['Year'].unique()
    for year in years:
        year_df = df_grouped[df_grouped['Year'] == year]
        fig_1 = px.pie(year_df, 
                        names='Sector', 
                        values='num_participants', 
                        title=f"Sector Distribution in {year}",
                        labels={'num_participants': 'Number of Participants', 'SECTOR': 'Sector'})
        fig_1.update_layout(width=600, height=600)
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
            title_x=0,
            title_y=0.95,
            xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
            yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))
        image_path_1 = os.path.join(output_folder, f"output_{year}_pie_chart.png")
        pio.write_image(fig_1, image_path_1)
        figures_1.append(fig_1)
    for fig in figures:
        graph_elements.append(dcc.Graph(figure=fig))
    for fig_1 in figures_1:
        graph_elements.append(dcc.Graph(figure=fig_1))
    return graph_elements

# @app.callback(
#     [Output('df-store', 'data'),
#      Output('output_message','children')], 
#     [Input('add-button', 'n_clicks'),
#      Input('update-button', 'n_clicks')],
#     [State('add-sector-input', 'value'),
#      State('add-year-input', 'value'),
#      State('add-month-input', 'value'),
#      State('add-participants-input', 'value'),
#      State('update-sector-dropdown', 'value'),
#      State('update-year-dropdown', 'value'),
#      State('update-month-dropdown', 'value'),
#      State('update-participants', 'value'),
#      State('df-store', 'data')]  
# )
def add_or_update_data(add_clicks, update_clicks, add_sector, add_year, add_month, add_num_participants,
                       update_sector, update_year, update_month, update_num_participants, stored_data):
    add_clicks = add_clicks or 0
    update_clicks = update_clicks or 0
    triggered_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0] if dash.callback_context.triggered else None
    if triggered_id == 'add-button':
        existing_data_check = check_existing_data(add_sector, add_month, add_year)
        if existing_data_check is not None:
             return  existing_data_check,"Data already exists for this Sector, Month, and Year"
        result = add_data_to_oracle(add_sector, add_year, add_month, add_num_participants)
        updated_df = fetch_data_from_oracle()
        return updated_df.to_dict('records'), 'Data added successfully'
    if triggered_id == 'update-button':
        result = update_data_in_oracle(update_sector, update_year, update_month, update_num_participants)
        updated_df = fetch_data_from_oracle()
        return updated_df.to_dict('records'), 'Data updated successfully'
    return stored_data,'' 

# @app.callback(
#     Output('search-results-table', 'data',allow_duplicate=True),
#     [Input('search-sector-dropdown', 'value'),
#      Input('search-year-dropdown', 'value'),
#      Input('search-month-dropdown', 'value'),
#      Input('df-store', 'data')]  
# )
def update_search_results(sector, year, month, stored_data):
    df_us= fetch_data_from_oracle()
    filtered_df = df_us[(df_us['Sector'] == sector) & (df_us['Year'] == year) & (df_us['Month'] == month)]
    if not filtered_df.empty:
        return filtered_df.to_dict('records')
    else:
        return []

# @app.callback(
#     [Output('search-sector-dropdown', 'options'),
#      Output('search-year-dropdown', 'options'),
#      Output('search-month-dropdown', 'options')],
#     [Input('df-store', 'data')]
# )
def update_dropdown_options(stored_data):
    df_ud = fetch_data_from_oracle()
    sectors = [{'label': sector, 'value': sector} for sector in df_ud['Sector'].unique()]
    years = [{'label': str(year), 'value': year} for year in df_ud['Year'].unique()]
    months = [{'label': month, 'value': month} for month in df_ud['Month'].unique()] 
    return sectors, years, months, sectors, years, months

# @app.callback(
#     [Output('update-sector-dropdown', 'options'),
#      Output('update-year-dropdown', 'options'),
#      Output('update-month-dropdown', 'options')],
#     [Input('df-store', 'data')]
# )
def update_dropdown_options_2(stored_data):
    df_ud = fetch_data_from_oracle()
    sectors = [{'label': sector, 'value': sector} for sector in df_ud['Sector'].unique()]
    years = [{'label': str(year), 'value': year} for year in df_ud['Year'].unique()]
    months = [{'label': month, 'value': month} for month in df_ud['Month'].unique()] 
    return sectors, years, months



# @app.callback(
#     [Output('search-results-table', 'data',allow_duplicate=True),
#      Output('df-store', 'data',allow_duplicate=True)],
#     [Input('search-results-table', 'data_previous')],
#     [State('search-results-table', 'data'),
#      State('df-store', 'data')]
# )
def delete_row(data_previous, current_data, stored_data):
    if not data_previous:
        raise PreventUpdate
    deleted_rows = []
    for row in data_previous:
        if row not in current_data:
            deleted_rows.append(row)
    if not deleted_rows:
        raise PreventUpdate
    for deleted_row in deleted_rows:
        print("Deleted Row:", deleted_row)
        sector = deleted_row['Sector']
        month = deleted_row['Month']
        year = deleted_row['Year']
        num_participants = deleted_row['num_participants']        
        print(f"Deleting record: {sector}, {month}, {year}, {num_participants}")
        delete_result = delete_record(sector, month, year, num_participants)     
        print("Delete result:", delete_result)
    updated_data = [row for row in stored_data if not (row['Sector'] == deleted_row['Sector'] and
                                                       row['Month'] == deleted_row['Month'] and
                                                       row['Year'] == deleted_row['Year'])]
    return updated_data, updated_data 

if __name__ == '__main__':
    app.run_server(debug=True)
    