import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import pandas as pd
import plotly.express as px
import numpy as np
from dash.dependencies import Input, Output
from pages.home_page_1 import home_1_plot,update_map


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

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




app.layout = html.Div(
    style={'backgroundColor': '#f0f4e1', 'padding': '20px'},
    children=[
        html.Div(home_1_plot()),
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
                html.Button('Calculate ACE Score', id='calculate-btn', n_clicks=0, 
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
    ]
)

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

@app.callback(
    Output('map-graph', 'figure'),
    Input('training-type-dropdown', 'value')
)
def show_home_plot_graph(selected_training_type):
    return update_map(selected_training_type)

if __name__ == '__main__':
    app.run_server(debug=True)
