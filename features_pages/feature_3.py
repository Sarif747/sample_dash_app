import pandas as pd
import numpy as np
import dash
from dash import html,dcc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
from features_pages.feature_3_1 import feature_3_1
from features_pages.feature_3_2 import feature_3_2,display_event_details,generate_calendar_markers

patient_groups = ['Group A', 'Group B', 'Group C', 'Group D', 'Group E']
n = len(patient_groups)

data = {
    'Patient Group ID': patient_groups,
    'Therapy Participation (%)': np.random.randint(60, 100, n),
    'Behavioral Improvement (Score)': np.random.uniform(3, 7, n),
    'Educational Engagement (%)': np.random.randint(50, 90, n),
}

df_progress = pd.DataFrame(data)

df_numeric = df_progress.select_dtypes(include=[np.number])

statistics = {
    'Mean Therapy Participation': df_progress['Therapy Participation (%)'].mean(),
    'Median Therapy Participation': df_progress['Therapy Participation (%)'].median(),
    'Std Dev Therapy Participation': df_progress['Therapy Participation (%)'].std(),
    
    'Mean Behavioral Improvement': df_progress['Behavioral Improvement (Score)'].mean(),
    'Median Behavioral Improvement': df_progress['Behavioral Improvement (Score)'].median(),
    'Std Dev Behavioral Improvement': df_progress['Behavioral Improvement (Score)'].std(),
    
    'Mean Educational Engagement': df_progress['Educational Engagement (%)'].mean(),
    'Median Educational Engagement': df_progress['Educational Engagement (%)'].median(),
    'Std Dev Educational Engagement': df_progress['Educational Engagement (%)'].std(),
}

correlation_matrix = df_numeric.corr()

fig_line = px.line(df_progress, x='Patient Group ID', y='Behavioral Improvement (Score)', 
                   title="Behavioral Improvements Over Time")
fig_line.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))

fig_bar = px.bar(df_progress, x='Patient Group ID', y=['Therapy Participation (%)', 'Educational Engagement (%)'],
                 barmode='stack', title="Therapy and Educational Engagement")
fig_bar.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))

fig_hist_therapy = px.histogram(df_progress, x='Therapy Participation (%)', nbins=10, title="Therapy Participation Distribution")
fig_hist_therapy.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))

fig_hist_behavior = px.histogram(df_progress, x='Behavioral Improvement (Score)', nbins=10, title="Behavioral Improvement Distribution")
fig_hist_behavior.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))

fig_hist_education = px.histogram(df_progress, x='Educational Engagement (%)', nbins=10, title="Educational Engagement Distribution")
fig_hist_education.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))

fig_corr = go.Figure(data=go.Heatmap(
    z=correlation_matrix.values,
    x=correlation_matrix.columns,
    y=correlation_matrix.index,
    colorscale='Viridis'
))
fig_corr.update_layout(title="Correlation Matrix", xaxis_title="Factors", yaxis_title="Factors")
fig_corr.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))
app = dash.Dash()

def feature_3():
    return html.Div([html.Div([
    html.H1("Progress Tracking Dashboard", style={
        'textAlign': 'left', 
        'color': 'darkgreen', 
        'fontWeight': 'bold'
    }),
    # html.Br(),
    dbc.Row([
        dbc.Col(
            html.Div(
                style={
                    'display': 'flex',
                    'justifyContent': 'space-between',  
                    'gap': '20px',  
                    'flex': 1, 
                    'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                    'borderRadius': '10px',
                    'padding': '10px',
                    'backgroundColor': 'white',
                    'margin': '20px auto',
                },
                children =[
                    dcc.Graph(id='line-chart', figure=fig_line,style={'flex': 1, 'height': '400px', 'margin': 'auto'}), 
                    dcc.Graph(id='progress-bar', figure=fig_bar,style={'flex': 1, 'height': '400px', 'margin': 'auto'}),
                ]
            ), width=12 
        ),
    ], justify="center", style={'marginBottom': '20px'}),

   html.Div([
    html.H4("Statistical Summary", style={
        'textAlign': 'left', 
        'color': 'darkgreen', 
        'fontSize': '24px', 
        'fontWeight': 'bold'
    }),
    html.Div([
        dbc.Row([
            dbc.Col(
                html.Div(
                    style={
                        'display': 'flex',
                        'justifyContent': 'space-between',  
                        'gap': '20px',  
                        'flex': 1, 
                        'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                        'borderRadius': '10px',
                        'padding': '10px',
                        'backgroundColor': 'white',
                        'margin': '20px auto',
                    },
                    children =[
                         html.Div([
                            html.P(f"Mean Therapy Participation: {statistics['Mean Therapy Participation']:.2f}%", style={'fontSize': '16px','color': 'darkgreen'}),
                            html.P(f"Median Therapy Participation: {statistics['Median Therapy Participation']:.2f}%", style={'fontSize': '16px','color': 'darkgreen'}),
                            html.P(f"Standard Deviation Therapy Participation: {statistics['Std Dev Therapy Participation']:.2f}", style={'fontSize': '16px','color': 'darkgreen'}),
                        ], style={'padding': '10px'}),
                        html.Div([
                            html.P(f"Mean Behavioral Improvement: {statistics['Mean Behavioral Improvement']:.2f}", style={'fontSize': '16px','color': 'darkgreen'}),
                            html.P(f"Median Behavioral Improvement: {statistics['Median Behavioral Improvement']:.2f}", style={'fontSize': '16px','color': 'darkgreen'}),
                            html.P(f"Standard Deviation Behavioral Improvement: {statistics['Std Dev Behavioral Improvement']:.2f}", style={'fontSize': '16px','color': 'darkgreen'}),
                        ], style={'padding': '10px'}),
                        html.Div([
                            html.P(f"Mean Educational Engagement: {statistics['Mean Educational Engagement']:.2f}%", style={'fontSize': '16px','color': 'darkgreen'}),
                            html.P(f"Median Educational Engagement: {statistics['Median Educational Engagement']:.2f}%", style={'fontSize': '16px','color': 'darkgreen'}),
                            html.P(f"Standard Deviation Educational Engagement: {statistics['Std Dev Educational Engagement']:.2f}", style={'fontSize': '16px','color': 'darkgreen'}),
                        ], style={'padding': '10px'}),
                    ]
                ),width=12
            ),
        ], justify="center", style={'marginBottom': '20px'}),  
    ], style={
        'padding': '20px', 
        'backgroundColor': '#f9f9f9', 
        'borderRadius': '10px', 
        'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)'
    }),
    ], style={'margin': '20px 0', 'padding': '10px'}),


    dbc.Row([
        dbc.Col(
            html.Div(
                style={
                    'display': 'flex',
                    'justifyContent': 'space-between',  
                    'gap': '20px',  
                    'flex': 1, 
                    'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                    'borderRadius': '10px',
                    'padding': '10px',
                    'backgroundColor': 'white',
                    'margin': '20px auto',
                },
                children =[
                    dcc.Graph(id='histogram-therapy', figure=fig_hist_therapy,style={'flex': 1, 'height': '400px', 'margin': 'auto'}), 
                    dcc.Graph(id='histogram-behavior', figure=fig_hist_behavior,style={'flex': 1, 'height': '400px', 'margin': 'auto'}),
                ]
            ), width=12 
        ),
    ], justify="center", style={'marginBottom': '30px'}),
    dbc.Row([
        dbc.Col(
            html.Div(
                style={
                    'display': 'flex',
                    'justifyContent': 'space-between',  
                    'gap': '20px',  
                    'flex': 1, 
                    'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                    'borderRadius': '10px',
                    'padding': '10px',
                    'backgroundColor': 'white',
                    'margin': '20px auto',
                },
                children =[
                    dcc.Graph(id='histogram-education', figure=fig_hist_education,style={'flex': 1, 'height': '400px', 'margin': 'auto'}), 
                    dcc.Graph(id='correlation-matrix', figure=fig_corr,style={'flex': 1, 'height': '400px', 'margin': 'auto'}),
                ]
            ), width=12 
        ),
    ], justify="center", style={'marginBottom': '30px'}),
], style={'backgroundColor': 'lightgreen', 'padding': '20px', 'minHeight': '100vh'}),
feature_3_1(),
feature_3_2()
])

# @app.callback(
#     Output('event-details', 'children'),
#     [Input('date-picker-range', 'start_date'),
#      Input('date-picker-range', 'end_date')]
# )
def event_details_display(start_date, end_date):
    return display_event_details(start_date, end_date)

# @app.callback(
#     Output('calendar', 'children'),
#     [Input('date-picker-range', 'start_date'),
#      Input('date-picker-range', 'end_date')]
# )
def calendar_markers_generator(start_date, end_date):
    return generate_calendar_markers(start_date, end_date)
if __name__ == '__main__':
    app.run_server(debug=True)
