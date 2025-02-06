import dash
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import random
from datetime import datetime, timedelta
from dash import dcc, html, dash_table
from features_pages.feature_2_2 import feature_2_2
from features_pages.feature_2_1 import feature_2_1

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

random.seed(42)

interventions = ['Therapy', 'Education', 'Family Support', 'Mental Health Counseling', 'Peer Support Groups', 
                 'Community Outreach Programs', 'Cognitive Behavioral Therapy (CBT)', 'Resilience Training']

outcome_types = ['Mental Health Score', 'Attendance Rate', 'Family Relationship Score', 
                 'School Performance (Grades)', 'Job Stability', 'Stress Levels', 
                 'Social Engagement', 'Emotional Well-being']


date_range = pd.date_range(start="2023-01-01", end="2023-12-31", freq='ME')

data = []
for intervention in interventions:
    for outcome in outcome_types:
        for date in date_range:
            outcome_value = random.randint(50, 100)
            trend_factor = np.sin((date.month / 12) * 2 * np.pi) 
            outcome_value += int(trend_factor * 10)  
            outcome_value = max(50, min(outcome_value, 100))
            data.append({
                'Date': date,
                'Intervention': intervention,
                'Outcome Measure': outcome,
                'Outcome Value': outcome_value
            })

df = pd.DataFrame(data)

avg_outcome_by_intervention = df.groupby('Intervention')['Outcome Value'].mean().reset_index()
fig_bar = px.bar(avg_outcome_by_intervention, x='Intervention', y='Outcome Value', 
                 title='Average Outcome Value by Intervention', color='Intervention')
fig_bar.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))

fig_box = px.box(df, x='Intervention', y='Outcome Value', color='Intervention', 
                 title='Distribution of Outcome Values by Intervention')
fig_box.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))

fig_hist = px.histogram(df, x='Outcome Value', color='Intervention', 
                        title='Distribution of Outcome Values', barmode='overlay')
fig_hist.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))

fig_scatter = px.scatter(df, x='Date', y='Outcome Value', color='Intervention', 
                         title='Outcome Value over Time', 
                         labels={'Date': 'Date', 'Outcome Value': 'Outcome Value'})
fig_scatter.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))

pivot_df = df.pivot_table(index='Intervention', columns='Outcome Measure', values='Outcome Value', aggfunc='mean')
fig_heatmap = px.imshow(pivot_df, title='Heatmap of Outcome Measures by Intervention')
fig_heatmap.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))

def feature_2():
    return html.Div([
    html.Div([
    html.H1(
        "Trauma-Informed Care Effectiveness",style={'textAlign': 'left', 'marginLeft': '25px', 'color': 'darkgreen'}
    ),
    html.Br(), 
    dbc.Row([
        dbc.Col(
            html.Div(
                dcc.Graph(id='bar-chart', figure=fig_bar), 
                style={
                    'padding': '15px', 
                    'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)', 
                    'borderRadius': '10px',
                    'backgroundColor': 'white'
                }
            ),
            width=6
        ),
        dbc.Col(
            html.Div(
                dcc.Graph(id='box-plot', figure=fig_box), 
                style={
                    'padding': '15px', 
                    'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)', 
                    'borderRadius': '10px',
                    'backgroundColor': 'white'
                }
            ),
            width=6
        ),
    ], justify="center", style={'marginBottom': '30px'}),

    dbc.Row([
        dbc.Col(
            html.Div(
                dcc.Graph(id='histogram', figure=fig_hist), 
                style={
                    'padding': '15px', 
                    'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)', 
                    'borderRadius': '10px',
                    'backgroundColor': 'white'
                }
            ),
            width=6
        ),
        dbc.Col(
            html.Div(
                dcc.Graph(id='scatter-plot', figure=fig_scatter), 
                style={
                    'padding': '15px', 
                    'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)', 
                    'borderRadius': '10px',
                    'backgroundColor': 'white'
                }
            ),
            width=6
        ),
    ], justify="center", style={'marginBottom': '30px'}),
    dbc.Row([
        dbc.Col(
            html.Div(
                dcc.Graph(id='heatmap', figure=fig_heatmap), 
                style={
                    'padding': '15px', 
                    'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)', 
                    'borderRadius': '10px',
                    'backgroundColor': 'white',
                    'width':'100%'
                }
            ),
            width=12
        ),
    ], justify="center"),
],style={'backgroundColor': 'lightgreen', 'padding': '20px','minHeight': '100vh'}
),
feature_2_1(),
feature_2_2()
])

if __name__ == '__main__':
    app.run_server(debug=True)
