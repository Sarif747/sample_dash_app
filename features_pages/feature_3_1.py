import pandas as pd
import numpy as np
import dash
from dash import html,dcc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

resources = ['Counseling', 'Workshop', 'Support Group', 'Educational Program']
patient_groups = ['Group A', 'Group B', 'Group C', 'Group D', 'Group E']

n = 20  

data = {
    'Patient Group ID': np.random.choice(patient_groups, n),
    'Resource': np.random.choice(resources, n),
    'Sessions Attended': np.random.randint(1, 10, n)  
}
df_resources = pd.DataFrame(data)

resource_ace_links = {
    "Counseling": {
        "ACE's Addressed": ['Emotional Abuse', 'Physical Abuse', 'Emotional Neglect'],
        "Link": 'https://www.counseling.org/ace'
    },
    "Workshop": {
        "ACE's Addressed": ['Household Dysfunction', 'Substance Abuse'],
        "Link": 'https://www.workshops.org/ace'
    },
    "Support Group": {
        "ACE's Addressed": ['Divorce', 'Mental Illness'],
        "Link": 'https://www.supportgroup.org/ace'
    },
    "Educational Program": {
        "ACE's Addressed": ['Physical Neglect', 'Witnessing Violence'],
        "Link": 'https://www.educationprogram.org/ace'
    }
}

fig_resource_bar = px.bar(df_resources, x='Resource', y='Sessions Attended', color='Resource', 
                          title="Resource Utilization by Patient Groups")
fig_resource_bar.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))

fig_pie = px.pie(df_resources.groupby('Patient Group ID').sum().reset_index(), 
                 names='Patient Group ID', values='Sessions Attended', 
                 title="Resource Utilization Distribution by Patient Groups")
fig_pie.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))

heatmap_data = df_resources.groupby(['Patient Group ID', 'Resource'])['Sessions Attended'].sum().unstack()
fig_heatmap = px.imshow(heatmap_data, title="Resource Utilization Heatmap")
fig_heatmap.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def feature_3_1():
    return html.Div([
    html.H1("Resource Utilization Analytics", style={'textAlign': 'left', 'marginLeft': '25px', 'color': 'darkgreen'}),
    dbc.Row([
        dbc.Col(
            html.Div(
                dcc.Graph(id='resource-bar', figure=fig_resource_bar), 
                style={
                    'padding': '10px', 
                    'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)', 
                    'borderRadius': '10px', 
                    'backgroundColor': 'white',
                    'width':'100%'
                }
            ),
            width=6
        ),
        html.Br(),
        dbc.Col(
            html.Div(
                dcc.Graph(id='resource-pie', figure=fig_pie), 
                style={
                    'padding': '10px', 
                    'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)', 
                    'borderRadius': '10px', 
                    'backgroundColor': 'white',
                    'width':'100%'
                }
            ),
            width=6
        ),
    ], justify="center", style={'marginBottom': '30px'}),
    dbc.Row([
         dbc.Col(
             html.Div(
                dcc.Graph(id='resource-heatmap', figure=fig_heatmap), 
                style={
                    'padding': '10px', 
                    'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)', 
                    'borderRadius': '10px', 
                    'backgroundColor': 'white',
                    'width':'100%'
                }
            ),
            width=12,
        ),
    ], justify="center", style={'marginBottom': '20px'}),
    html.Div([
        html.H4("Resource Links", style={
            'textAlign': 'left', 
            'color': 'darkgreen', 
            'fontWeight': 'bold'
         }),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5(resource, style={'fontWeight': 'bold', 'fontSize': '18px'})),
                    dbc.CardBody([
                        html.P(f"ACE's Addressed: {', '.join(details['ACE\'s Addressed'])}", style={'fontSize': '14px', 'color': 'darkgreen'}),
                        html.A("Learn More", href=details['Link'], target="_blank", style={
                            'textDecoration': 'underline', 
                            'color': 'blue', 
                            'fontSize': '16px'
                        })
                    ])
                ], style={
                    'margin': '10px', 
                    'padding': '20px', 
                    'borderRadius': '8px',
                    'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
                    'transition': 'transform 0.3s ease-in-out',
                    'cursor': 'pointer',
                    'backgroundColor': 'white',
                })
            ], width=3, style={'marginBottom': '20px'})
            for resource, details in resource_ace_links.items()
        ], justify="start", style={
            # 'display': 'flex',
            'flexWrap': 'wrap',
            'justifyContent': 'space-around',
            'gap': '20px',
        })
    ], style={'marginTop': '20px', 'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)','width':'98.5%'}),

], style={'backgroundColor': '#f0f4e1', 'padding': '40px', 'minHeight': '100vh'})


if __name__ == '__main__':
    app.run_server(debug=True)
