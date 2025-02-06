from dash import Dash, dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import random
from datetime import datetime, timedelta

# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

random.seed(42)

sectors = ['Schools', 'Hospitals', 'Social Services', 'Community Outreach']

regions = ['North', 'South', 'East', 'West']

date_range = pd.date_range(start="2023-01-01", end="2023-12-31", freq='ME')

data = []
for sector in sectors:
    for region in regions:
        for date in date_range:
            adoption_rate = random.randint(40, 90)
            trend_factor = np.sin((date.month / 12) * 2 * np.pi)  
            adoption_rate += int(trend_factor * 5)  
            adoption_rate = max(40, min(adoption_rate, 90))
            data.append({
                'Date': date,
                'Sector': sector,
                'Region': region,
                'Adoption Rate': adoption_rate
            })

df_adoption = pd.DataFrame(data)
fig_line = px.line(df_adoption, x='Date', y='Adoption Rate', color='Sector', 
                   title='Adoption Rate of Trauma-Informed Practices Over Time')
fig_line.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))

fig_bar_adoption = px.bar(df_adoption.groupby('Sector')['Adoption Rate'].mean().reset_index(), 
                          x='Sector', y='Adoption Rate', 
                          title='Average Adoption Rate by Sector', color='Sector')
fig_bar_adoption.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))

fig_box_adoption = px.box(df_adoption, x='Sector', y='Adoption Rate', color='Sector', 
                          title='Distribution of Adoption Rates by Sector')
fig_box_adoption.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))

pivot_adoption = df_adoption.pivot_table(index='Sector', columns='Region', values='Adoption Rate', aggfunc='mean')
fig_heatmap_adoption = px.imshow(pivot_adoption, title='Heatmap of Adoption Rates by Region and Sector')
fig_heatmap_adoption.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))

fig_hist_adoption = px.histogram(df_adoption, x='Adoption Rate', color='Sector', 
                                  title='Distribution of Adoption Rates', barmode='overlay')
fig_hist_adoption.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))

def feature_2_1():
    return html.Div([
    html.H1(
        "Trauma-Informed Care Adoption Tracking",style={'textAlign': 'left', 'marginLeft': '25px', 'color': 'darkgreen'}
    ),
    html.Br(),
    dbc.Row([
        dbc.Col(
            html.Div(
                dcc.Graph(id='bar-chart-adoption', figure=fig_bar_adoption), 
                style={
                    'padding': '10px', 
                    'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)', 
                    'borderRadius': '10px', 
                    'backgroundColor': 'white'
                }
            ),
            width=6
        ),
        dbc.Col(
            html.Div(
                dcc.Graph(id='heatmap-adoption', figure=fig_heatmap_adoption), 
                style={
                    'padding': '10px', 
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
                dcc.Graph(id='box-plot-adoption', figure=fig_box_adoption), 
                style={
                    'padding': '10px', 
                    'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)', 
                    'borderRadius': '10px', 
                    'backgroundColor': 'white'
                }
            ),
            width=6
        ),
        dbc.Col(
            html.Div(
                dcc.Graph(id='histogram-adoption', figure=fig_hist_adoption), 
                style={
                    'padding': '10px', 
                    'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)', 
                    'borderRadius': '10px', 
                    'backgroundColor': 'white'
                }
            ),
            width=6
        ),
    ], justify="center", style={'marginBottom': '30px'}),  

], style={'backgroundColor': '#f0f4e1', 'padding': '40px', 'minHeight': '100vh'})  


# if __name__ == '__main__':
#     app.run_server(debug=True)
