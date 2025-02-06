import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash import dash_table
import pandas as pd
import io
import base64
import dash_bootstrap_components as dbc

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True, prevent_initial_callbacks='initial_duplicate')

def testing_page_3():
    return  html.Div(
    children=[
        html.H1(
            "Modeify and generate excel files",
            style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}
        ),
        html.H6("This section you can upload an unfinished excel or csv file and you can add, delete or update the excel file and you can download the excel file",style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
        dcc.Upload(
            id='upload-data_1',
            children=html.Button(
                'Upload Excel File', 
                style={
                    'padding': '10px 20px',
                    'borderRadius': '5px',
                    'backgroundColor': '#4CAF50', 
                    'color': 'white',  
                    'border': 'none',
                    'cursor': 'pointer',
                    'fontWeight': 'bold',
                    'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.2)'
                }
            ),
            multiple=False,
            accept='.csv, .xlsx',
            style={
                'display': 'flex',
                'justifyContent': 'center',
                'margin': '20px auto',
                'width': 'auto'
            }
        ),
        html.Div(
            id='file-data-table',
        ),
        html.Div(
            id='input-fields',
            children=[],
            style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center', 'gap': '15px'} 
        ),
        html.Br(),
        html.Div(
            id='dynamic-buttons',
            children=[],
        ),
        html.Div(
            id='save-data-message',
            children=[],
        )
    ]
)

df = pd.DataFrame()

# @app.callback(
#     Output('file-data-table', 'children',allow_duplicate=True),
#     Output('input-fields', 'children'),
#     Output('dynamic-buttons', 'children',allow_duplicate=True),  
#     Input('upload-data', 'contents'),
#     State('upload-data', 'filename'),
# )
def upload_file(contents, filename):
    global df
    if contents is None:
        return dash.no_update, dash.no_update, dash.no_update
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(decoded))
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(io.BytesIO(decoded), engine='openpyxl')
        else:
            return f"Unsupported file type: {filename}", dash.no_update, {'display': 'none'}
        table = html.Div(dash_table.DataTable(
            id='uploaded-data-table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
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
                    },)
        input_fields = []
        row = []
        for i, column in enumerate(df.columns):
            row.append(
                dbc.Col(
                    html.Div([
                        html.Label(f"Enter {column}:", style={'textAlign': 'left', 'marginLeft': '20px', 'color': 'darkgreen'}),
                        dcc.Input(id=f'{column}-input', value='', type='text', debounce=True,
                                  style={'width': '150px', 'height': '40px', 'textAlign': 'center', 'color': 'darkgreen'}),
                    ]),
                    width=8,  
                )
            )
            if (i + 1) % 4 == 0 or (i + 1) == len(df.columns): 
                input_fields.append(dbc.Row(row, style={'marginBottom': '20px'}))
                row = []  
        dynamic_buttons = html.Div([
            html.Button('Add New Data', id='add-new-data-button', n_clicks=0,style={
                                    'width': '200px',
                                    'height': '40px',
                                    'textAlign': 'center',
                                    'color': 'darkgreen',
                                }),
            html.Button('Save Data', id='save-data-button', n_clicks=0,style={
                                    'width': '200px',
                                    'height': '40px',
                                    'textAlign': 'center',
                                    'color': 'darkgreen',
                                }),
            html.Button('Download as Excel', id='download-button', n_clicks=0,style={
                                    'width': '200px',
                                    'height': '40px',
                                    'textAlign': 'center',
                                    'color': 'darkgreen',
                                }),
            dcc.Download(id='download-data')
        ],style={
                        'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                        'borderRadius': '10px',
                        'padding': '10px',
                        'backgroundColor': 'white',
                        'margin': '20px auto',
                        'width': '100%',
                        'display': 'flex', 
                        'alignItems': 'center',  
                        'gap': '20px', 
                    })
        return table, input_fields, dynamic_buttons
    except Exception as e:
        return f'Error reading the file: {str(e)}', dash.no_update, dash.no_update

# @app.callback(
#     Output('file-data-table', 'children'),
#     Output('save-data-message', 'children',allow_duplicate=True),
#     Input('add-new-data-button', 'n_clicks'),
#     State('uploaded-data-table', 'data'),
#     State('uploaded-data-table', 'columns'),
#     State('input-fields', 'children'),
# )
def add_new_data(n_clicks, data, columns, input_fields):
    global df
    if n_clicks > 0:
        new_row = {}
        for field in input_fields:
            field_id = field['props']['children'][1]['props']['id']
            new_row[field_id.replace('-input', '')] = field['props']['children'][1]['props']['value']
        df.loc[len(df)] = new_row
        return "New data added successfully!" ,dash_table.DataTable(
            id='uploaded-data-table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            editable=True,
            row_deletable=True,
            style_table={'height': '300px', 'overflowY': 'auto'},
        )
    return dash.no_update,dash.no_update


# @app.callback(
#     Output('save-data-message', 'children'),
#     Output('dynamic-buttons', 'children'), 
#     Input('save-data-button', 'n_clicks'),
#     State('uploaded-data-table', 'data'),
#     State('uploaded-data-table', 'columns')
# )
def save_data(n_clicks, data, columns):
    global df
    if n_clicks > 0:
        df = pd.DataFrame(data, columns=[col['name'] for col in columns])
        dynamic_buttons = html.Div([
            html.Button('Add New Data', id='add-new-data-button', n_clicks=0,style={
                                    'width': '200px',
                                    'height': '40px',
                                    'textAlign': 'center',
                                    'color': 'darkgreen',
                                }),
            html.Button('Save Data', id='save-data-button', n_clicks=0,style={
                                    'width': '200px',
                                    'height': '40px',
                                    'textAlign': 'center',
                                    'color': 'darkgreen',
                                }),
            html.Button('Download as Excel', id='download-button', n_clicks=0,style={
                                    'width': '200px',
                                    'height': '40px',
                                    'textAlign': 'center',
                                    'color': 'darkgreen',
                                }),
            dcc.Download(id='download-data')
        ],style={
                        'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                        'borderRadius': '10px',
                        'padding': '10px',
                        'backgroundColor': 'white',
                        'margin': '20px auto',
                        'width': '100%',
                        'display': 'flex', 
                        'alignItems': 'center',  
                        'gap': '20px', 
                    })
        return 'Data saved successfully!', dynamic_buttons
    return dash.no_update, dash.no_update

# @app.callback(
#     Output('download-data', 'data'),
#     Input('download-button', 'n_clicks'),
# )
def download_excel(n_clicks):
    if n_clicks > 0:
        excel_file = io.BytesIO()
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        excel_file.seek(0)
        return dcc.send_data_frame(df.to_excel, "modified_data.xlsx")
    return dash.no_update

# if __name__ == '__main__':
#     app.run_server(debug=True)
