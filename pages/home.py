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


data = {
    "Date": [
        "March 25, 2022",
        "April 22, 2022",
        "April 26, 2022",
        "June 2, 2022",
        "November 1, 2022",
        "November 3, 2022",
        "November 10, 2022",
        "December 2, 2022",
        "January 2023 (Planned)",
        "February 2023 (Planned)",
        "February 2023 (Planned)"
    ],
    "Counties Served": [
        "Clarke, Oconee, Madison, Jackson",
        "Morgan County",
        "Clarke County",
        "Madison County",
        "Madison, Elbert, Oglethorpe",
        "Barrow, Jackson, Walton, Oconee",
        "Greene County",
        "Newton County",
        "Clarke County",
        "Morgan, Jasper, Greene",
        "All 12 counties in the region"
    ],
    "Participants": [
        24,
        None,
        15,
        37,
        19,
        20,
        10,
        50,
        None,
        None,
        13
    ],
    "Training Type": [
        "CRMI",
        "YMHAW",
        "CRMI",
        "CRMW",
        "CRMW",
        "CMW",
        "CRMI",
        "ACE/CRM",
        "ACE/CRM",
        "ACE/CRM",
        "CSFT"
    ]
}

def home():
   
    df = pd.DataFrame(data)

   
    df_filtered = df[df['Participants'].notnull()]

   
    fig = go.Figure()
    green_colors = ['#d9f0d3', '#c8e6c9', '#a5d6a7', '#81c784', '#66bb6a', '#4caf50']
   
    fig.add_trace(go.Bar(
        x=df_filtered['Training Type'],
        y=df_filtered['Participants'],
        marker_color=green_colors[:len(df_filtered)],
        hoverinfo='text',
        hovertemplate='<b>Training Type:</b> %{x}<br>' +
                    '<b>Participants:</b> %{y}<extra></extra>',
        opacity=0.8,
        name='Participants',
        text=df_filtered['Participants'],
        textposition='auto',
    ))

    fig.update_layout(
        title='Participants in Different Training Types',
        title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
        title_x=0,  
        title_y=1, 
        xaxis_title='Training Type',
        xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
        yaxis_title='Number of Participants',
        yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
        barmode='group',
        height=400,
        margin=dict(l=40, r=40, t=60, b=40),
        plot_bgcolor='rgba(255, 255, 255, 0)',  
    )
    fig.update_traces(marker=dict(line=dict(width=2, color='rgba(0, 0, 0, 0.3)')))

    return html.Div([
        html.H2(
            "Training Overview",
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
                        id='home-graph',
                        figure=fig,
                        style={'width': '100%', 'height': '400px', 'margin': 'auto'}
                    )
                ]
                )),
        dbc.Col(
            html.Div(
                [
                    html.H2('COALITION TRAININGS',style={'textAlign': 'left', 'marginLeft': '0px', 'color': 'darkgreen'}),
                    html.P("In 2022, Resilient Northeast Georgia has honed its training approach to be more county-specific by"
                            "splitting the region into clusters determined by geographic proximity, thematic similarity of"
                            "strategic plans, areas of interest for collaborative expansion, and the leadership and insights of the"
                            "regional manager. As a result, the collaborative focused energy on smaller, more specialized"
                            "training modalities than years past, prioritizing depth of impact and usability of skills acquired in"
                            "the training in an effort to improve sustainability of retained regional knowledge over time."),
                        html.Strong("Note**\n"),
                        html.P(
                        "CRMI - Community Resiliency Model Introduction\n"
                        "YMHAW - Youth Mental Health First Aid Workshop\n"
                        "CRMW - Community Resiliency Model Workshop\n"
                        "CMW - Connections Matter Workshop\n"
                        "ACE/CRM - The Business Case for ACE's/CRM Intro Hybrid\n"
                        "CSFT - Circle of Security Facilitator Training",
                        style={'whiteSpace': 'pre-line'}
                    )
                ],
            )),
        ])],
        style={'backgroundColor': 'lightgreen', 'padding': '20px'}
        )
        


data_1 = {
    "Sector": [
        "First Responders",
        "Healthcare Providers",
        "Faith-Based Leaders",
        "Juvenile Justice Organizations",
        "Early Childhood and Education",
        "Youth-Serving Organizations",
        "Public Health/Social Services",
        "School Employees",
        "Parents/Caregivers",
        "Business Owners/Employees",
        "Post-Secondary Educators"
    ],
    "December 2021": [1, 3, 4, 1, 3, 12, 7, 3, 2, 4, 3],
    "June 2022": [6, 9, 5, 8, 13, 13, 29, 17, 8, 4, 20]
}

def plot_two():
    df_1 = pd.DataFrame(data_1)

    df_long = pd.melt(df_1, id_vars=['Sector'], value_vars=['December 2021', 'June 2022'],
                      var_name='Month', value_name='Participation')

    fig_1 = px.line(
        df_long,
        x='Sector',
        y='Participation',
        color='Month', 
        text='Participation',
        title='Sector Participation: December 2021 vs. June 2022',
        labels={'Sector': 'Sector', 'Participation': 'Participation'},
        template='plotly',
        color_discrete_sequence=['#e1f5e0', '#c8e6c9'] 
    )

    fig_1.update_traces(mode='lines+markers',
                        line=dict(color='black'),
                        marker=dict(size=10, opacity=0.3),
                        textposition='top center')

    fig_1.update_layout(
        margin=dict(l=40, r=40, t=40, b=40),
        paper_bgcolor='rgba(255, 255, 255, 0)',  
        plot_bgcolor='rgba(255, 255, 255, 0)',
        title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
        title_x=0,  
        title_y=1, 
        xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
        yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    )
    return html.Div([
           html.H2(
                "Growing Coallation",
                style={'textAlign': 'right', 'marginRight': '50px', 'color': 'darkgreen'}
                ),
            dbc.Row([
            dbc.Col(
                html.Div(
                    [
                        html.H2("True Collaboration as a Determining Factor for Success",style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
                        html.P("While event engagement was strong prior to the coalition's partnership with Family Connection, the diversity and depth of participation in regional coalition initiatives has significantly increased as this partnership has grown over time, in part due to",style={'textAlign': 'left', 'marginLeft': '50px'}),
                        html.Ul([
                            html.Li("Expansion of the regional footprint, from six counties to twelve counties"),
                            html.Li("Expertise of trusted leaders, knowledgeable in community needs and capacity"),
                            html.Li("Inclusion of existing networks, creating a deeper well of engaged participants"),
                            html.Li("Growth of the coalition resource bank, spearheaded by regional experts"),
                            html.Li("Incorporation of new partners, who contribute a variety of new resources"),
                            html.Li("Development of relationships, brokered by Family Connection's regional manager")
                        ],style={'textAlign': 'left', 'marginLeft': '50px'})
                    ],
                )),
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
                            id='line-plot', figure=fig_1,
                            style={'width': '100%', 'height': '400px', 'margin': 'auto'}
                        )
                    ]
                    )),
            ])],
            #  style={'backgroundColor': '#f0f4e1', 'padding': '20px'}
             style={'backgroundColor': '#f0f4e1', 'padding': '20px'}
            )

data_2 = {
    "Type of Support": [
        "Trainings",
        "Connections and Partnerships",
        "Resources",
        "Awareness/Education Tools",
        "Networking Opportunities"
    ],
    "Responses": [77, 67, 65, 61, 55],
    "Percentage": [76.2, 66.3, 64.4, 60.4, 54.5]  
}

def plot_three():
    df_2 = pd.DataFrame(data_2)

    fig_2 = go.Figure()

 
    fig_2.add_trace(go.Bar(
        x=df_2['Type of Support'],
        y=df_2['Responses'],
        marker_color='rgba(33, 254, 48, 0.6)',  
        hoverinfo='text',
        hovertemplate='<b>Type of Support:</b> %{x}<br>' +
                      '<b>Responses:</b> %{y}<extra></extra>',
        opacity=0.8,
        name='Responses',
        text=df_2['Responses'],
        textposition='auto',
    ))

    fig_2.add_trace(go.Scatter(
        x=df_2['Type of Support'],
        y=df_2['Percentage'],
        mode='lines+markers',
        name='Percentage',
        line=dict(color='black', width=2),
        marker=dict(size=8),
        hoverinfo='text',
        hovertemplate='<b>Type of Support:</b> %{x}<br>' +
                      '<b>Percentage:</b> %{y}%<extra></extra>',
    ))

    fig_2.update_layout(
        title='Responses to Types of Support',
        title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
        title_x=0,  
        title_y=0.95, 
        xaxis_title='Type of Support',
        xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
        yaxis_title='Number of Responses',
        yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
        height=400,
        margin=dict(l=40, r=40, t=60, b=40),
        plot_bgcolor='rgba(255, 255, 255, 0)',  
    )

    fig_2.update_layout(
        yaxis2=dict(
            title='Percentage',
            overlaying='y',
            side='right',
            range=[0, 100], 
            showgrid=False,
            title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold')
        )
    )

    fig_2.update_traces(marker=dict(line=dict(width=2, color='rgba(0, 0, 0, 0.3)')))

    return html.Div([
        html.H2(
            "Types of Support Responses",
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
                            id='bar-plot', figure=fig_2,
                            style={'width': '100%', 'height': '400px', 'margin': 'auto'}
                        )
                    ]
                )),
            dbc.Col(
                html.Div(
                    [
                        html.H2(" STRONGER TOGETHER",style={'textAlign': 'left', 'marginLeft': '0px', 'color': 'darkgreen'}),
                        html.P("What does it mean to be Stronger Together? As a coalition, Resilient Northeast Georgia believes that when we work together to improve the health and well-being of our communities, we are stronger together. When we embrace ways of thinking that center on the strengths and resources that exist in our communities rather than the gaps and barriers, we are stronger"
                                "together. When we find ways to alleviate the effects of past, present, and"
                                "future childhood trauma in our communities, we are stronger together. Our"
                                "interconnectedness as partners and our plans for common action make us"
                                "stronger together as a region",style={'textAlign': 'left', 'marginLeft': '0px'}),
                        html.P("What can Resilient Northeast Georgia provide to help your county's trauma informed efforts?",style={'textAlign': 'left', 'marginLeft': '0px'})
                    ],
                )),
            ])],
        style={'backgroundColor': 'lightgreen', 'padding': '20px'}
    )

knowledge_data = {
    "Category": [
        "Understanding of Trauma",
        "Understanding of Resiliency",
        "Regional Connectivity",
        "Enhanced Strategies",
        "Tangible Next Steps"
    ],
    "Pre-Survey": [55.1, 53.1, 17.0, 8.5, 6.4],
    "Post-Survey": [70.3, 71.3, 71.3, 64.4, 57.4],
    "Increase (%)": [27.4, 34.0, 319.4, 657.7, 796.9]
}

def plot_knowledge():
    df_knowledge = pd.DataFrame(knowledge_data)

    fig_knowledge = go.Figure()

    fig_knowledge.add_trace(go.Bar(
        x=df_knowledge['Category'],
        y=df_knowledge['Pre-Survey'],
        name='Pre-Survey',
        marker_color='rgba(33, 254, 48, 0.6)',
        hoverinfo='text',
        hovertemplate='<b>Category:</b> %{x}<br>' +
                      '<b>Pre-Survey:</b> %{y}<extra></extra>',
        opacity=0.8,
        text=df_knowledge['Pre-Survey'],
        textposition='auto',
    ))

    fig_knowledge.add_trace(go.Bar(
        x=df_knowledge['Category'],
        y=df_knowledge['Post-Survey'],
        name='Post-Survey',
        marker_color='rgba(0, 128, 0, 0.6)',  
        hoverinfo='text',
        hovertemplate='<b>Category:</b> %{x}<br>' +
                      '<b>Post-Survey:</b> %{y}<extra></extra>',
        opacity=0.8,
        text=df_knowledge['Post-Survey'],
        textposition='auto',
    ))

    fig_knowledge.add_trace(go.Scatter(
        x=df_knowledge['Category'],
        y=df_knowledge['Increase (%)'],
        mode='lines+markers',
        name='Increase (%)',
        line=dict(color='black', width=2),
        marker=dict(size=8),
        hoverinfo='text',
        hovertemplate='<b>Category:</b> %{x}<br>' +
                        '<b>Increase (%):</b> %{y}%<extra></extra>',
    ))

    fig_knowledge.update_layout(
            yaxis=dict(range=[0, 900]),  
        )
    fig_knowledge.update_layout(
        title='Knowledge Gains from Pre-Survey to Post-Survey',
        title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
        title_x=0,
        title_y=0.95,
        xaxis_title='Category',
        xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
        yaxis_title='Scores',
        yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
        height=400,
        margin=dict(l=40, r=40, t=60, b=40),
        plot_bgcolor='rgba(255, 255, 255, 0)',
    )

    fig_knowledge.update_layout(
        yaxis2=dict(
            title='Increase (%)',
            overlaying='y',
            side='right',
            range=[0, max(df_knowledge['Increase (%)']) + 100],
            showgrid=False,
            title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold')
        )
    )

    return html.Div([
        html.H2(
            "OVERVIEW OF FINDINGS (STRONGER TOGETHER SURVEY RESULTS)",
            style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}
        ),
        dbc.Row([
            # dbc.Col(
            #     html.Div(
            #         [
            #             html.H2("STRONGER TOGETHER SURVEY RESULTS",style={'textAlign': 'left', 'marginLeft': '50px', 'color': 'darkgreen'}),
            #         ],
            #     )),
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
                            id='knowledge-plot', figure=fig_knowledge,
                            style={'width': '100%', 'height': '400px', 'margin': 'auto'}
                        )
                    ]
                )),
        ]),
    ],
        style={'backgroundColor': '#f0f4e1', 'padding': '20px'}  
    )
