import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from dash_bootstrap_components._components.Container import Container
import dash
from dash import dcc, html
import numpy as np
import plotly.express as px
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

years = [2019, 2020, 2021, 2022, 2023, 2024]
categories = [
    "Evaluation Costs", "Partner Incentives", "Marketing and Website",
    "Programs/Initiatives", "Grant Administration", "Collaborative Meetings and Summit",
    "Training Costs", "Resilient Georgia Admin Fee", "Project Management"
]

expenditures = [
    [3330.81, 19375.55, 3059.19, 12136.29, 20702.25, 8661.02, 19785.08, 8000.00, 40000.00],
    [3513.95, 20371.33, 3212.25, 12743.01, 21737.36, 9094.07, 20177.07, 8500.00, 41000.00],
    [3694.89, 21389.83, 3372.87, 13375.56, 22824.23, 9548.67, 20595.66, 9000.00, 42000.00],
    [4050.00, 24446.26, 3953.72, 15726.11, 26701.30, 10933.32, 25313.45, 10000.00, 44993.02],
    [4252.50, 25668.57, 4151.41, 16512.43, 28036.37, 11480.00, 26598.12, 11000.00, 46000.00],
    [4465.12, 26951.99, 4358.98, 17337.06, 29438.19, 12054.00, 27902.03, 12000.00, 47000.00]
]

df_ML_Model = pd.DataFrame(expenditures, columns=categories, index=years)

X = np.array(years).reshape(-1, 1)  


def predict_future(year_to_predict):
    model = LinearRegression()
    predictions = {}
    for category in categories:
        y = df_expenditures[category].values  
        model.fit(X, y)
        future_year = np.array([[year_to_predict]])
        predicted_value = model.predict(future_year)[0]
        predictions[category] = predicted_value

    return predictions

df_expenditures = pd.DataFrame(expenditures, columns=categories, index=years).reset_index()
df_long = pd.melt(df_expenditures, id_vars=['index'], var_name='Category', value_name='Expenditure')
df_long.rename(columns={'index': 'Year'}, inplace=True)

def create_expenditure_graph():
    fig_expenditures = px.line(
        df_long,
        x='Year',
        y='Expenditure',
        color='Category',
        title='Expenditures Over Years by Category',
        labels={'Year': 'Year', 'Expenditure': 'Expenditure'},
        template='plotly',
        color_discrete_sequence=px.colors.qualitative.Set1
    )

    fig_expenditures.update_traces(mode='lines+markers',
                                    line=dict(width=2),
                                    marker=dict(size=8),
                                    textposition='top center')

    fig_expenditures.update_layout(
        margin=dict(l=40, r=40, t=40, b=40),
        paper_bgcolor='rgba(255, 255, 255, 0)',  
        plot_bgcolor='rgba(255, 255, 255, 0)',
        title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
        title_x=0,  
        title_y=0.95, 
        xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
        yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    )

    return html.Div([
        html.H2("Expenditures by Category Over the Years",
                                style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
                        html.P("This graph illustrates the changes in expenditures across various categories from 2019 to 2024.",
                               style={'textAlign': 'left', 'marginLeft': '50px'}),
        dbc.Row([
            dbc.Col(
                html.Div([
                html.H3("Select Year",style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
                dcc.Slider(
                    id='year-slider',
                    min=min(years),
                    max=max(years),
                    value=max(years),
                    marks={year: str(year) for year in years},
                    step=1
                ),
            ],style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'},)),
            dbc.Col(
                [
                    dcc.Checklist(
                        style={
                            'display': 'inline-block',
                            'alignItems': 'center',
                            'margin': '20px 0',
                            'padding': '5px 10px',
                            'border': '1px solid darkgreen',
                            'borderRadius': '5px',
                            'backgroundColor': '#f0f4e1'
                        },
                        inputStyle={'marginRight': '10px'},
                        labelStyle={
                            'fontSize': '16px',
                            'color': 'darkgreen',
                            'fontWeight': 'bold',
                            'margin': '5px 0'
                        },
                        id='show-all-checkbox',
                        options=[
                            {'label': '  Show All Years', 'value': 'ALL'},
                        ],
                        value=[],
                        inline=True, 
                    ),
                ]
            )
        ]),
        dbc.Row(html.Div(
                    style={
                        'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                        'borderRadius': '10px',
                        'padding': '10px',
                        'backgroundColor': 'white',
                        'margin': '20px auto',
                        'width': '100%',
                    },
                    children=[
                        dcc.Graph(
                            id='expenditure-plot',
                            style={'width': '100%', 'height': '400px', 'margin': 'auto'}
                        )
                    ]
                )),
        dbc.Row(html.Div([
            html.H2("Predict Future Expenditure", style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
            dcc.Dropdown(
                style={
                    'width': '200px',
                    'height': '40px',
                    'marginLeft': '25px', 
                    'textAlign': 'left',
                    'color': 'darkgreen'  
                },
                className='dropdown-center',
                id='year-dropdown-predict',
                options=[{'label': str(year), 'value': year} for year in range(2015, 2031)],
                value=2022,
                clearable=False,
            ),
            html.Button('Predict', id='predict-button', n_clicks=0,className='btn btn-primary',  
                                style={
                                    'fontSize': '16px',
                                    'fontWeight': 'bold',
                                    'borderRadius': '5px',
                                    'padding': '10px 20px',
                                    'margin': '20px',
                                    'backgroundColor': 'darkgreen',  
                                    'color': 'white',
                                    'border': 'none',
                                    'cursor': 'pointer',
                                    'transition': 'background-color 0.3s ease',
                                    'textAlign': 'left', 'marginLeft': '50px',
                                }),
            html.Div(id='prediction-output', style={'marginTop': '20px'})
            ], style={'backgroundColor': '#f0f4e1', 'padding': '20px'})),
    ],
    style={'backgroundColor': '#f0f4e1', 'padding': '20px'}
    )

def expenditure_plot(selected_year,show_all, predicted_values):

    if 'ALL' in show_all:
        fig_expenditures = px.line(
            df_long,
            x='Category',
            y='Expenditure',
            title='Expenditures by Category for All Years',
            labels={'Category': 'Category', 'Expenditure': 'Expenditure'},
            template='plotly',
            color='Year', 
            color_discrete_sequence=px.colors.qualitative.Set1
        )
    else:
        filtered_data = df_long[df_long['Year'] == selected_year]
        fig_expenditures = px.line(
            filtered_data,
            x='Category',
            y='Expenditure',
            title=f'Expenditures by Category in {selected_year}',
            labels={'Category': 'Category', 'Expenditure': 'Expenditure'},
            template='plotly',
            color_discrete_sequence=px.colors.qualitative.Set1
        )
        if predicted_values:
            predicted_data = pd.DataFrame(predicted_values.items(), columns=['Category', 'Predicted Expenditure'])
            predicted_data['Year'] = selected_year  
            fig_expenditures.add_scatter(
                x=predicted_data['Category'],
                y=predicted_data['Predicted Expenditure'],
                mode='lines+markers',
                name='Predicted Expenditure',
                line=dict(color='red', dash='dash')
            )

    fig_expenditures.update_traces(mode='lines+markers',
                                    line=dict(width=2),
                                    marker=dict(size=8),
                                    textposition='top center')

    fig_expenditures.update_layout(
        margin=dict(l=40, r=40, t=40, b=40),
        paper_bgcolor='rgba(255, 255, 255, 0)',
        plot_bgcolor='rgba(255, 255, 255, 0)',
        title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
        title_x=0,
        title_y=0.95,
        xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
        yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    )

    return fig_expenditures


def issues_overview():
    
    issues = [
        "Fear", "Anxiety", "Loneliness", "Depression", "Hopelessness", 
        "Drug use (non-opioid)", "Alcohol use", "Falling out of recovery", 
        "Loss of self-esteem", "Loss of control", "Overdose", "Opioid Use", 
        "Eating Disorders", "Intimate Partner Violence", "PTSD", "Suicide"
    ]
    
    data = [
        [2, 3, 59], [1, 4, 58], [1, 4.5, 57], [1, 5, 56], [1, 10, 50],
        [0, 10, 50], [0, 13, 48], [2, 12, 47], [0, 17, 47], [1, 16, 56],
        [1, 15, 46], [1, 14, 46], [1, 12, 46], [1, 19, 43], [3, 18, 42], [2, 17, 42]
    ]
    
    df_issues = pd.DataFrame(data, columns=["Severity", "Frequency", "Impact"])
    df_issues['Issues'] = issues
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_issues['Issues'],
        y=df_issues['Severity'],
        marker_color='rgba(33, 254, 48, 0.6)',  
        hoverinfo='text',
        hovertemplate='<b>Issue:</b> %{x}<br>' +
                      '<b>Severity:</b> %{y}<extra></extra>',
        opacity=0.8,
        name='Severity',
        text=df_issues['Severity'],
        textposition='auto',
    ))

    fig.add_trace(go.Bar(
        x=df_issues['Issues'],
        y=df_issues['Frequency'],
        marker_color='rgba(33, 254, 48, 0.6)',  
        hoverinfo='text',
        hovertemplate='<b>Issue:</b> %{x}<br>' +
                      '<b>Frequency:</b> %{y}<extra></extra>',
        opacity=0.8,
        name='Frequency',
        text=df_issues['Frequency'],
        textposition='auto',
    ))

    fig.update_layout(
        title='Overview of Issues',
        title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
        xaxis_title='Issues',
        xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
        yaxis_title='Scores',
        yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
        barmode='group',
        height=400,
        margin=dict(l=40, r=40, t=60, b=40),
        plot_bgcolor='rgba(255, 255, 255, 0)',
    )
    
    return html.Div([
        html.H2(
            "Issues Overview",
            style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}
        ),
        dbc.Row([
            dbc.Col(
                html.Div(
                    style={
                        'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                        'borderRadius': '10px',
                        'padding': '10px',
                        'backgroundColor': 'white',
                        'margin': '20px auto',
                        'width': '90%',
                    },
                    children=[
                        dcc.Graph(
                            id='issues-graph',
                            figure=fig,
                            style={'width': '100%', 'height': '400px', 'margin': 'auto'}
                        )
                    ]
                )
            ),
            dbc.Col(
                html.Div(
                    [
                        html.H2('ISSUES EXPLAINED', style={'textAlign': 'left', 'marginLeft': '0px', 'color': 'darkgreen'}),
                        html.P("This overview highlights various mental health and social issues affecting individuals in the community."
                                " Each issue is quantified by severity and frequency, providing insight into the areas that may need attention."
                                " The data helps in understanding the urgency and prevalence of these challenges."),
                        html.Strong("Definitions:\n"),
                        html.P(
                            "Severity: A measure of the impact or seriousness of the issue.\n"
                            "Frequency: How often the issue occurs in the population.",
                            style={'whiteSpace': 'pre-line'}
                        )
                    ],
                ),width=4
            ),
        ])
    ],
    style={'backgroundColor': 'lightgreen', 'padding': '20px'}
    )