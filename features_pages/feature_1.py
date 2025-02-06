import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import numpy as np
import plotly.express as px
import pandas as pd
import random
from datetime import datetime, timedelta
from dash import dash_table
import plotly.io as pio

county_coordinates = {
    "Clarke County": (33.9519, -83.3576),
    "Oconee County": (33.8679, -83.4372),
    "Madison County": (34.0993, -83.2195),
    "Jackson County": (34.1176, -83.5495),
    "Morgan County": (33.6174, -83.5962),
    "Barrow County": (34.0143, -83.6887),
    "Walton County": (33.7705, -83.7209),
    "Greene County": (33.5707, -83.1292),
    "Newton County": (33.5540, -83.8610),
    "Jasper County": (33.0018, -83.7350),
    "Hall County": (34.3036, -83.7650),
    "Habersham County": (34.5990, -83.5541)
}

def generate_synthetic_data(start_year, end_year, num_entries):
    synthetic_data = {
        "Date": [],
        "Counties Served": [],
        "Participants": [],
        "Training Type": []
    }
    counties = list(county_coordinates.keys())
    training_types = ["CRMI", "YMHAW", "CRMW", "CMW", "ACE/CRM", "CSFT"]
    for _ in range(num_entries):
        random_days = random.randint(0, (datetime(end_year, 12, 31) - datetime(start_year, 1, 1)).days)
        random_date = (datetime(start_year, 1, 1) + timedelta(days=random_days)).strftime("%Y-%m-%d")
        synthetic_data["Date"].append(random_date)
        synthetic_data["Counties Served"].append(random.choice(counties))
        synthetic_data["Participants"].append(random.randint(5, 50))
        synthetic_data["Training Type"].append(random.choice(training_types))
    return synthetic_data

synthetic_data = generate_synthetic_data(2019, 2024, 100)
df = pd.DataFrame(synthetic_data)

county_data = df.groupby('Counties Served').agg(
    total_participants=('Participants', 'sum'),
    training_types=('Training Type', 'unique')
).reset_index()

county_data['Latitude'] = county_data['Counties Served'].apply(lambda x: county_coordinates.get(x, (0, 0))[0])
county_data['Longitude'] = county_data['Counties Served'].apply(lambda x: county_coordinates.get(x, (0, 0))[1])

avg_lat = county_data['Latitude'].mean()
avg_lon = county_data['Longitude'].mean()

lat_range = county_data['Latitude'].max() - county_data['Latitude'].min()
lon_range = county_data['Longitude'].max() - county_data['Longitude'].min()

zoom_level = 9  
if lat_range < 0.5 and lon_range < 0.5:
    zoom_level = 10  
elif lat_range < 1 and lon_range < 1:
    zoom_level = 8  
elif lat_range < 2 and lon_range < 2:
    zoom_level = 7  
else:
    zoom_level = 6  

fig_map = px.density_mapbox(
    county_data,
    lat='Latitude',
    lon='Longitude',
    z='total_participants',
    hover_name='Counties Served',
    hover_data=['training_types'],
    color_continuous_scale=[
        [0, 'rgb(255, 255, 255)'],  
        [0.5, 'rgb(0, 0, 255)'],    
        [1, 'rgb(0, 0, 128)']       
    ],  
    mapbox_style="carto-positron",
    # mapbox_style="carto-darkmatter",
    zoom=zoom_level,
    center={"lat": avg_lat, "lon": avg_lon},
    title='ACEs Prevalence and Training Participation in Georgia Counties',
   
)

fig_map.update_layout(
    title='ACEs Prevalence and Training Participation in Georgia Counties',
    title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold') 
)

fig_scatter = px.scatter(
    df,
    x='Date',
    y='Participants',
    color='Training Type',
    hover_name='Counties Served',
    title='Participants by Date, County, and Training Type',
    labels={'Participants': 'Total Participants'},
)

fig_scatter.update_layout(
    title='Participants by Date, County, and Training Type',
    title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    hovermode='closest',
    plot_bgcolor='rgba(255, 255, 255, 0)',
)

fig_scatter.update_xaxes(
    title_text='Date',
    title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    tickformat='%Y'
)

fig_scatter.update_yaxes(
    title_text='Total Participants',
    title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold')
)

questions = [
    "Did a parent or other adult in the household often or very often swear at you, insult you, put you down, or humiliate you? OR Act in a way that made you afraid that you might be physically hurt?",
    "Did a parent or other adult in the household often or very often push, grab, slap, or throw something at you? OR Ever hit you so hard that you had marks or were injured?",
    "Did an adult or person at least five years older than you ever touch or fondle you or have you touch their body in a sexual way? OR Attempt or actually have oral, anal, or vaginal intercourse with you?",
    "Did you often or very often feel that no one in your family loved you or thought you were important or special? OR Your family didn’t look out for each other, feel close to each other, or support each other?",
    "Did you often or very often feel that you didn’t have enough to eat, had to wear dirty clothes, and had no one to protect you? OR Your parents were too drunk or high to take care of you or take you to the doctor if you needed it?",
    "Were your parents ever separated or divorced?",
    "Was your mother or stepmother often or very often pushed, grabbed, slapped, or had something thrown at her? OR Sometimes, often, or very often, kicked, bitten, hit with a fist, or hit with something hard? OR Ever repeatedly hit for at least a few minutes or threatened with a gun or knife?",
    "Did you live with anyone who was a problem drinker or alcoholic, or who used street drugs?",
    "Was a household member depressed or mentally ill, or did a household member attempt suicide?",
    "Did a household member go to prison?"
]

issues = [
    "Fear", "Anxiety", "Loneliness", "Depression", "Hopelessness", 
    "Drug use (non-opioid)", "Alcohol use", "Falling out of recovery", 
    "Loss of self-esteem", "Loss of control", "Overdose", "Opioid Use", 
    "Eating Disorders", "Intimate Partner Violence", "PTSD", "Suicide"
]

np.random.seed(42)  

severity = np.random.normal(loc=2, scale=2, size=len(issues))  
frequency = np.random.normal(loc=10, scale=3, size=len(issues))  
impact = np.random.normal(loc=50, scale=10, size=len(issues))  

df_issues = pd.DataFrame({
    "Severity": severity,
    "Frequency": frequency,
    "Impact": impact,
    "Issues": issues
})

fig_severity = px.bar(df_issues, x='Issues', y='Severity', title="Severity of Issues")
fig_frequency = px.bar(df_issues, x='Issues', y='Frequency', title="Frequency of Issues")
fig_impact = px.bar(df_issues, x='Issues', y='Impact', title="Impact of Issues")

fig_scatter = px.scatter(df_issues, x='Severity', y='Frequency', size='Impact', color='Issues', 
                         title="Scatter Plot of Severity vs Frequency with Impact Size", 
                         labels={"Severity": "Severity", "Frequency": "Frequency"})

fig_severity.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),)
fig_frequency.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),)
fig_impact.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),)
fig_scatter.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),)


fig_severity.update_traces(marker=dict(color='darkgreen'))
fig_frequency.update_traces(marker=dict(color='lightgreen'))
fig_impact.update_traces(marker=dict(color='green'))

data = {
    "Mental Health": [
        {"question": "Felt depressed, sad, or withdrawn", "experienced 1 or more days in past 30 days": 485362, "experienced all 30 days": 56983},
        {"question": "Felt suddenly overwhelmed with fear", "experienced 1 or more days in past 30 days": 244198, "experienced all 30 days": 17556},
        {"question": "Experienced severely out-of-control behavior", "experienced 1 or more days in past 30 days": 141177, "experienced all 30 days": 14053},
        {"question": "Avoided food, threw up, or used laxatives", "experienced 1 or more days in past 30 days": 167636, "experienced all 30 days": 17369},
        {"question": "Experienced intense anxiety, worries or fears", "experienced 1 or more days in past 30 days": 368073, "experienced all 30 days": 52847},
        {"question": "Experienced extreme difficulty concentrating", "experienced 1 or more days in past 30 days": 222237, "experienced all 30 days": 38445},
        {"question": "Experienced severe mood swings", "experienced 1 or more days in past 30 days": 264998, "experienced all 30 days": 30812},
        {"question": "Experienced drastic changes in behavior", "experienced 1 or more days in past 30 days": 268940, "experienced all 30 days": 31062},
    ],
    "Suicidality": [
        {"question": "Seriously considered attempting suicide", "considered attempted": 104362, "more than 5 times": 24117},
        {"question": "Attempted suicide", "considered attempted": 54182, "more than 5 times": 10667},
    ],
    "Self-Harm": [
        {"question": "Seriously considered self-harming", "considered self harm": 162971, "more than 5 times": 44640},
        {"question": "Self-harmed", "considered self harm": 54526, "more than 5 times": 23107},
    ]
}

mental_health_df = pd.DataFrame(data["Mental Health"])
suicidality_df = pd.DataFrame(data["Suicidality"])
self_harm_df = pd.DataFrame(data["Self-Harm"])

fig_mental_health = px.bar(
    mental_health_df,
    x='question',
    y=['experienced 1 or more days in past 30 days', 'experienced all 30 days'],
    title="Mental Health Issues",
    labels={'value': 'Number of Students', 'question': 'Survey Question'},
)

fig_suicidality = px.bar(
    suicidality_df,
    x='question',
    y=['considered attempted', 'more than 5 times'],
    title="Suicidality Issues",
    labels={'value': 'Number of Students', 'question': 'Survey Question'},
)

fig_self_harm = px.bar(
    self_harm_df,
    x='question',
    y=['considered self harm', 'more than 5 times'],
    title="Self-Harm Issues",
    labels={'value': 'Number of Students', 'question': 'Survey Question'},
)

fig_mental_health.update_layout(barmode='group',plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))
fig_suicidality.update_layout(barmode='group',plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))
fig_self_harm.update_layout(barmode='group',plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True, prevent_initial_callbacks='initial_duplicate')

 
def feature_1():
 return  html.Div([
    html.Div([
        html.H1("ACEs Prevalence Heatmap", style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
        dbc.Row([
            dbc.Col(
                html.Div(
                    style={
                        'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.3)', 
                        'borderRadius': '10px',
                        'padding': '10px',
                        'backgroundColor': 'white',
                        'margin': '20px auto',
                        'width': '100%',
                    },
                    children=[
                        dcc.Graph(
                            id='map-graph',
                            figure=fig_map,
                            style={'width': '100%', 'height': '600px', 'margin': 'auto'}
                        ),
                    ]
                ), width=12
            ),
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H3('Training and Program Details', style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
                    html.Div(id='county-info', style={
                        'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.3)', 
                        'borderRadius': '10px',
                        'padding': '10px',
                        'backgroundColor': 'white',
                        'margin': '20px auto',
                        'width': '100%',
                        'fontSize': '16px'
                    })
                ]),
                width=12
            ),
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    # html.H3('Edit Training Data for County', style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
                    dash_table.DataTable(
                        id='county-table',
                        columns=[
                            {'name': 'Date', 'id': 'Date', 'editable': True},
                            {'name': 'Counties Served', 'id': 'Counties Served', 'editable': False},
                            {'name': 'Participants', 'id': 'Participants', 'editable': True},
                            {'name': 'Training Type', 'id': 'Training Type', 'editable': True}
                        ],
                        data=[],  
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
                        ]
                    ),
                ], style={
                    'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.1)',  
                    'borderRadius': '10px',
                    'padding': '10px',
                    'backgroundColor': 'white',
                    'margin': '20px auto',
                    'width': '100%',
                }),
                width=12
            ),
        ]),
        # dbc.Row([
        #     dbc.Col(
        #         html.Div(
        #             dcc.Graph(
        #                 id='scatter-graph',
        #                 figure=fig_scatter,
        #                 style={'width': '100%', 'height': '500px', 'margin': 'auto'}
        #             )
        #         ),style={
        #                 'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
        #                 'borderRadius': '10px',
        #                 'padding': '10px',
        #                 'backgroundColor': 'white',
        #                 'margin': '20px auto',
        #                 'width': '80%',
        #             },
        #     )
        # ])
        ], style={
        'backgroundColor': 'lightgreen','padding': '20px',}),
    html.Div(
        style={'backgroundColor': '#f0f4e1', 'padding': '20px'},
        children=[
            html.H2(
                "OVERVIEW OF FINDINGS (STRONGER TOGETHER SURVEY RESULTS)",
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
                            'width': '100%',
                        },
                        children=[
                            dcc.Graph(
                                id='severity-plot', figure=fig_severity,
                                style={'width': '100%', 'height': '400px', 'margin': 'auto'}
                            ),
                        ]
                    )
                ),
                dbc.Col(
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
                            dcc.Graph(
                                id='frequency-plot', figure=fig_frequency,
                                style={'width': '100%', 'height': '400px', 'margin': 'auto'}
                            ),
                        ]
                    )
                ),
                dbc.Col(
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
                            dcc.Graph(
                                id='impact-plot', figure=fig_impact,
                                style={'width': '100%', 'height': '400px', 'margin': 'auto'}
                            ),
                        ]
                    )
                ),
            ]),

            dbc.Row([
                dbc.Col(
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
                            dcc.Graph(
                                id='scatter-plot', figure=fig_scatter,
                                style={'width': '100%', 'height': '600px', 'margin': 'auto'}
                            ),
                        ]
                    )
                ),
            ]),
            html.H2(
                "Overview of Georgia Student Health Survey 2022-2023",
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
                            'width': '100%',
                        },
                        children=[
                            dcc.Graph(
                                id='mental-health-plot', figure=fig_mental_health,
                                style={'width': '90%', 'height': '600px', 'margin': 'auto'}
                            ),
                        ]
                    )
                ),
            ]),

            dbc.Row([
                dbc.Col(
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
                            dcc.Graph(
                                id='suicidality-plot', figure=fig_suicidality,
                                style={'width': '100%', 'height': '400px', 'margin': 'auto'}
                            ),
                        ]
                    )
                ),
                dbc.Col(
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
                            dcc.Graph(
                                id='self-harm-plot', figure=fig_self_harm,
                                style={'width': '100%', 'height': '400px', 'margin': 'auto'}
                            ),
                        ]
                    )
                ),
            ]),
        html.H2(
            "ACE Score Calculation",
            style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}
        ),
        dbc.Row([
            dbc.Col(children=[
                html.Div(
                    style={
                        'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                        'borderRadius': '10px',
                        'padding': '20px',
                        'backgroundColor': 'white',
                        'margin': '10px auto',
                        'width': '100%',
                    },
                    children=[  
                        html.Div([
                            html.H4(question),
                            dcc.RadioItems(
                                id=f"q{i+1}",
                                options=[
                                    {'label': 'Yes', 'value': 1},
                                    {'label': 'No', 'value': 0}
                                ],
                                value=None,
                                style={
                                    'marginTop': '10px',
                                    'display': 'flex', 
                                    'flexDirection': 'row',  
                                    'alignItems': 'center',  
                                    'justifyContent': 'flex-start',  
                                    'fontSize': '16px',  
                                    'color': 'darkgreen',  
                                },
                                labelStyle={
                                    'fontSize': '16px',  
                                    'paddingRight': '15px',  
                                }
                            ),
                            html.Br()  
                        ]) for i, question in enumerate(questions)
                    ]
                ),
                html.Div([
                    dbc.Button('Calculate ACE Score', id='calculate-btn', n_clicks=0, 
                                style={
                                    'width': '40%', 
                                    'padding': '10px', 
                                    'backgroundColor': 'darkgreen', 
                                    'color': 'white', 
                                    'border': 'none', 
                                    'borderRadius': '5px',
                                    'display': 'block',  
                                    'margin': '0 auto'  
                                })
                ], style={
                    'paddingTop': '30px', 
                    'display': 'flex',  
                    'justifyContent': 'center',  
                    'alignItems': 'center'  
                }
                ),
                html.Div(id='result', style={
                    'paddingTop': '30px', 'textAlign': 'center', 'fontSize': '24px', 'color': 'darkblue'
                }),
                html.Div(id='resources', style={'display': 'none', 'paddingTop': '30px', 'textAlign': 'center'}, children=[
                    html.H4("Resources for ACEs:", style={'color': 'darkgreen'}),
                    html.Div(id='resource-link', style={'fontSize': '18px'})
                ])
        ])
        ]),
])])

@app.callback(
    [Output('county-info', 'children'),
     Output('county-table', 'data')],
    [Input('map-graph', 'hoverData')]
)
def display_county_info(hoverData):
    if hoverData is None:
        return "Hover over a county to see training programs and participants.", []
    county_name = hoverData['points'][0]['hovertext']
    county_info = county_data[county_data['Counties Served'] == county_name].iloc[0]
    training_list = ', '.join(county_info['training_types'])
    county_specific_data = df[df['Counties Served'] == county_name]
    table_data = county_specific_data.to_dict('records')
    return f"In {county_name}, the following training programs have been conducted: {training_list}. Total Participants: {county_info['total_participants']}.", table_data

@app.callback(
    Output('county-table', 'data', allow_duplicate=True),
    [Input('county-table', 'data_previous')],
    [State('county-table', 'data')]
)
def update_table_data(data_previous, data):
    if data_previous is None:
        return data
    return data

@app.callback(
    [Output('result', 'children'),
     Output('resources', 'style'),
     Output('resource-link', 'children')],
    Input('calculate-btn', 'n_clicks'),
    [Input(f"q{i+1}", 'value') for i in range(len(questions))]
)
def calculate_ace_score(n_clicks, *answers):
    if n_clicks > 0:
        ace_score = sum(answers)
        if ace_score <= 3:
            resource_link = html.A(
                "General ACEs Information (Low Risk)", 
                href="https://www.cdc.gov/violenceprevention/childabuseandneglect/acestudy/index.html", 
                target="_blank",
                style={'color': 'darkblue', 'fontSize': '20px'}
            )
        elif 4 <= ace_score <= 6:
            resource_link = html.A(
                "Managing ACEs (Moderate Risk)", 
                href="https://www.cdc.gov/violenceprevention/aces/fastfacts.html", 
                target="_blank",
                style={'color': 'darkblue', 'fontSize': '20px'}
            )
        else:
            resource_link = html.A(
                "Support Services for High ACEs (High Risk)", 
                href="https://www.mentalhealth.gov/what-to-look-for/mental-health-conditions", 
                target="_blank",
                style={'color': 'darkblue', 'fontSize': '20px'}
            )  
        resources_style = {'display': 'block', 'paddingTop': '30px'}   
        return f"Your ACE score is: {ace_score}", resources_style, resource_link
    return "", {'display': 'none'}, ""


if __name__ == '__main__':
    app.run_server(debug=True)
