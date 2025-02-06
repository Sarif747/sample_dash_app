import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash import dash_table
import pandas as pd
import plotly.express as px
import base64
import io
import os
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True, prevent_initial_callbacks='initial_duplicate')

def graph_layout():
    return html.Div([
        html.H2("Upload Excel or CSV File and Create Graphs", style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
        html.H6("This is section you can upload an excel file which consists of data and can select the axis which you want to create graphs based on axis selection it will show what type of graphs you can create in the graph type dropdown",style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
        dbc.Row([
            dbc.Col(
            dcc.Upload(
                    id='upload-data',
                    children=html.Button('Upload Excel or CSV File'),
                    multiple=False,
                    style={
                            'width': '200px',
                            'height': '40px',
                            'textAlign': 'center',
                            'color': 'darkgreen',
                        }
             ),
            ),
            html.Div(id='output-data-upload'),
            dbc.Col([  
                html.Div([
                        html.Label("Select Axis", style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
                        dcc.Dropdown(id='axis-dropdown', multi=True, placeholder="Select Axis", style={
                            'width': '600px', 'height': '40px', 'textAlign': 'center', 'color': 'darkgreen'
                        }),
                        html.Label("Select Graph Type",style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
                        dcc.Dropdown(
                            id='graph-type-dropdown',
                            multi=True,
                            placeholder="Select Graph Type",
                            style={
                                'width': '600px',
                                'height': '40px',
                                'textAlign': 'center',
                                'color': 'darkgreen',
                             },
                        ),
                ],style={
                            'display': 'flex',
                            'flexDirection': 'row', 
                            'justifyContent': 'flex-start',  
                            'alignItems': 'center', 
                            'gap': '5px',  
                        }),
            ]),
        ]),
        dbc.Row(),
        dbc.Row([
            dbc.Col(
                    html.Div(
                            id='graph-output',  
                    ),style={
                            'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                            'borderRadius': '10px',
                            'padding': '10px',
                            'backgroundColor': 'white',
                            'margin': '20px auto',
                            'width': '80%',
                        },
                )
            ]),
        ], style={'backgroundColor': '#f0f4e1', 'padding': '20px'})

def parse_file(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    file_extension = os.path.splitext(filename)[1].lower()
    if file_extension in ['.xlsx', '.xls']:
        try:
            df = pd.read_excel(io.BytesIO(decoded), engine='openpyxl') if file_extension == '.xlsx' else pd.read_excel(io.BytesIO(decoded), engine='xlrd')
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            raise e
    elif file_extension == '.csv':
        try:
            df = pd.read_csv(io.BytesIO(decoded))
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            raise e
    else:
        raise ValueError("Unsupported file format. Please upload a valid Excel (.xls/.xlsx) or CSV file.")
    return df

# @app.callback(
#     [Output('output-data-upload', 'children', allow_duplicate=True),
#      Output('graph-output', 'children', allow_duplicate=True),
#      Output('axis-dropdown', 'options')],
#     [Input('upload-data', 'contents')],
#     [State('upload-data', 'filename')]
# )
def update_output(uploaded_file, filename):
    if uploaded_file is None:
        return html.Div("No file uploaded yet."), {}, []
    print('arif')
    df = parse_file(uploaded_file, filename)
    print(df)
    table = dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'name': col, 'id': col} for col in df.columns],
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
        page_size=10
    )
    column_options = [{'label': col, 'value': col} for col in df.columns]
    fig = {}
    print(column_options)
    return html.Div([table]), dcc.Graph(figure=fig), column_options

# @app.callback(
#     Output('graph-type-dropdown', 'options'),
#     Output('graph-type-dropdown', 'placeholder'),
#     Input('axis-dropdown', 'value')
# )
def update_graph_types(selected_columns):
    if not selected_columns:
        return [], "Select Columns"
    graph_options = []
    if len(selected_columns) == 1:
        graph_options = [
            {'label': 'Pie Chart', 'value': 'pie'},
            {'label': 'Histogram', 'value': 'histogram'},
            {'label': 'Box Plot', 'value': 'box'},
        ]
    elif len(selected_columns) == 2:
        graph_options = [
            {'label': 'Scatter Plot', 'value': 'scatter'},
            {'label': 'Line Plot', 'value': 'line'},
            {'label': 'Bar Chart', 'value': 'bar'},
            {'label': 'Bubble Chart', 'value': 'bubble'},
        ]
    elif len(selected_columns) == 3:
        graph_options = [
            {'label': '3D Scatter Plot', 'value': '3dscatter'},
            {'label': 'Line Plot', 'value': 'line'},
            {'label': 'Bubble Chart', 'value': 'bubble'},
        ]
    else:
        graph_options = [
            {'label': 'Heatmap', 'value': 'heatmap'},
            {'label': 'Correlation Matrix', 'value': 'corrmatrix'},
        ]
    return graph_options, "Select Graph Type"

# @app.callback(
#     Output('graph-output', 'children', allow_duplicate=True),
#     [Input('axis-dropdown', 'value'),
#      Input('graph-type-dropdown', 'value')],
#     [State('upload-data', 'contents')],
#     [State('upload-data', 'filename')]
# )
def update_graph(axis_col, graph_types, uploaded_file,filename):
    if uploaded_file is None or not graph_types:
        fig = {}
        return dcc.Graph(figure=fig) 
    df = parse_file(uploaded_file, filename)
    figures = []
    print('arif_1')
    print(graph_types)
    if isinstance(graph_types, list):
        try:
            for graph in graph_types:
                if graph == 'pie' and len(axis_col) == 1:
                    fig = px.pie(df, names=axis_col[0], title=f"Pie Chart: {axis_col[0]}")
                    fig.update_layout(barmode='group',plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
                            title_x=0,
                            title_y=0.95,
                            xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
                            yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))
                    figures.append(dcc.Graph(figure=fig))

                if graph == 'histogram' and len(axis_col) == 1:
                    fig = px.histogram(df, x=axis_col[0], title=f"Histogram: {axis_col[0]}")
                    fig.update_layout(barmode='group',plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
                            title_x=0,
                            title_y=0.95,
                            xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
                            yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))
                    figures.append(dcc.Graph(figure=fig))
                
                if graph == 'box' and len(axis_col) == 1:
                    fig = px.box(df, y=axis_col[0], title=f"Box Plot: {axis_col[0]}")
                    fig.update_layout(barmode='group',plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
                            title_x=0,
                            title_y=0.95,
                            xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
                            yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))
                    figures.append(dcc.Graph(figure=fig))

                if graph == 'scatter' and len(axis_col) == 2:
                    print('arif')
                    fig = px.scatter(df, x=axis_col[0], y=axis_col[1], title=f"Scatter Plot: {axis_col[0]} vs {axis_col[1]}")
                    fig.update_layout(barmode='group',plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
                            title_x=0,
                            title_y=0.95,
                            xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
                            yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))
                    figures.append(dcc.Graph(figure=fig))
                if graph == 'line' and len(axis_col) == 2:
                    fig = px.line(df, x=axis_col[0], y=axis_col[1], title=f"Line Plot: {axis_col[0]} vs {axis_col[1]}")
                    fig.update_layout(barmode='group',plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
                            title_x=0,
                            title_y=0.95,
                            xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
                            yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))
                    figures.append(dcc.Graph(figure=fig))

                if graph == 'bar' and len(axis_col) == 2:
                    fig = px.bar(df, x=axis_col[0], y=axis_col[1], title=f"Bar Plot: {axis_col[0]} vs {axis_col[1]}")
                    fig.update_layout(barmode='group',plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
                            title_x=0,
                            title_y=0.95,
                            xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
                            yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))
                    figures.append(dcc.Graph(figure=fig))

                if graph == 'bubble' and len(axis_col) == 2:
                    if pd.api.types.is_numeric_dtype(df[axis_col[1]]):
                        fig = px.scatter(df, x=axis_col[0], y=axis_col[1], size=df[axis_col[1]], title=f"Bubble Chart: {axis_col[0]} vs {axis_col[1]}")
                        fig.update_layout(barmode='group',plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
                            title_x=0,
                            title_y=0.95,
                            xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
                            yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))
                    else:
                        fig = px.scatter(df, x=axis_col[0], y=axis_col[1], size=df[axis_col[0]], title=f"Bubble Chart: {axis_col[0]} vs {axis_col[1]}")
                        fig.update_layout(barmode='group',plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
                            title_x=0,
                            title_y=0.95,
                            xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
                            yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))
                    figures.append(dcc.Graph(figure=fig))
                
                if graph == '3dscatter' and len(axis_col) == 3:
                    fig = px.scatter_3d(df, x=axis_col[0], y=axis_col[1], z=axis_col[2], title=f"3D Scatter Plot: {axis_col[0]} vs {axis_col[1]} vs {axis_col[2]}")
                    fig.update_layout(barmode='group',plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
                            title_x=0,
                            title_y=0.95,
                            xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
                            yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))
                    figures.append(dcc.Graph(figure=fig))
            
                if graph == 'line' and len(axis_col) == 3:
                    fig = px.line(df, x=axis_col[0], y=axis_col[1], line_group=axis_col[2], title=f"Line Plot: {axis_col[0]} vs {axis_col[1]} with {axis_col[2]}")
                    fig.update_layout(barmode='group',plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
                            title_x=0,
                            title_y=0.95,
                            xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
                            yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))
                    figures.append(dcc.Graph(figure=fig))
            
                if graph == 'heatmap' and len(axis_col) >= 3:
                    numeric_df = df.select_dtypes(include=['number'])
                    if numeric_df.empty:
                        fig = go.Figure()
                        fig.add_annotation(
                            x=0.5, y=0.5,
                            text="Unable to load the graph. No numeric data available.",
                            showarrow=False,
                            font=dict(size=15, color="red"),
                            align="center"
                        )
                        figures.append(dcc.Graph(figure=fig))
                    else:
                        try:
                            fig = px.imshow(numeric_df.corr(), color_continuous_scale='RdBu', title="Correlation Matrix")
                            fig.update_layout(barmode='group',plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
                                    title_x=0,
                                    title_y=0.95,
                                    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
                                    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))
                            figures.append(dcc.Graph(figure=fig))
                        except Exception as e:
                            fig = go.Figure()
                            fig.add_annotation(
                                x=0.5, y=0.5,
                                text="Unable to load the graph. Error calculating correlation.",
                                showarrow=False,
                                font=dict(size=15, color="red"),
                                align="center"
                            )
                            figures.append(dcc.Graph(figure=fig))

                if graph == 'corrmatrix' and len(axis_col) >= 3:
                    numeric_df = df.select_dtypes(include=['number'])
                    if numeric_df.empty:
                        fig = go.Figure()
                        fig.add_annotation(
                            x=0.5, y=0.5,
                            text="Unable to load the graph. No numeric data available.",
                            showarrow=False,
                            font=dict(size=15, color="red"),
                            align="center"
                        )
                        figures.append(dcc.Graph(figure=fig))
                    else:
                        try:
                            fig = px.imshow(df.corr(), color_continuous_scale='RdBu', title="Correlation Matrix")
                            fig.update_layout(barmode='group',plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
                                    title_x=0,
                                    title_y=0.95,
                                    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
                                    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))
                            figures.append(dcc.Graph(figure=fig))
                        except Exception as e:
                            fig = go.Figure()
                            fig.add_annotation(
                                x=0.5, y=0.5,
                                text="Unable to load the graph. Error calculating correlation.",
                                showarrow=False,
                                font=dict(size=15, color="red"),
                                align="center"
                            )
                            figures.append(dcc.Graph(figure=fig))
        except Exception as e:
                        fig = go.Figure()
                        fig.add_annotation(
                            x=0.5, y=0.5,
                            text="Unable to load the graph. Error calculating",
                            showarrow=False,
                            font=dict(size=15, color="red"),
                            align="center"
                        )
                        figures.append(dcc.Graph(figure=fig))
    if figures:
        return figures  
    return "unable to load the Graph" 

# if __name__ == '__main__':
#     app.run_server(debug=True)