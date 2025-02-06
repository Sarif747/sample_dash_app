from dash import Dash, dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import random
import plotly.express as px
from wordcloud import WordCloud
import plotly.graph_objects as go
from textblob import TextBlob

# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

random.seed(42)

roles = ['Teacher', 'Parent', 'Healthcare Worker']

feedback_data = []
for role in roles:
    for i in range(100):  
        feedback_text = random.choice([
            "The training was very helpful and informative.",
            "I feel better equipped to deal with trauma in the classroom.",
            "It was a waste of time, and I did not learn much.",
            "The program is effective, but more time should be allocated to it.",
            "I learned useful techniques, but the content was overwhelming.",
            "The training was too basic, needs more depth.",
            "I appreciate the approach, but it could be more interactive."
        ])
        feedback_data.append({
            'Role': role,
            'Feedback': feedback_text
        })

df_feedback = pd.DataFrame(feedback_data)

def get_sentiment(text):
    analysis = TextBlob(text)
    score = analysis.sentiment.polarity  
    if score > 0.1:
        return 'Positive'
    elif score < -0.1:
        return 'Negative'
    else:
        return 'Neutral'

df_feedback['Sentiment'] = df_feedback['Feedback'].apply(get_sentiment)
df_feedback['Sentiment Score'] = df_feedback['Feedback'].apply(lambda x: TextBlob(x).sentiment.polarity)

wordcloud = WordCloud(background_color='white',width=800, height=400, max_words=200).generate(' '.join(df_feedback['Feedback']))
wordcloud_image = wordcloud.to_image()

fig_sentiment = px.bar(df_feedback['Sentiment'].value_counts(), 
                       title="Sentiment Distribution of Feedback",
                       labels={'value': 'Count', 'Sentiment': 'Sentiment'},
                       color=df_feedback['Sentiment'].value_counts().index)
fig_sentiment.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))

sentiment_counts = df_feedback['Sentiment'].value_counts().reset_index()
sentiment_counts.columns = ['Sentiment', 'Count']  
fig_pie = px.pie(sentiment_counts, names='Sentiment', values='Count', title='Feedback Sentiment Distribution')
fig_pie.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))

fig_hist_sentiment = px.histogram(df_feedback, x='Sentiment Score', nbins=20, 
                                  title='Distribution of Sentiment Scores')
fig_hist_sentiment.update_layout(plot_bgcolor='white', paper_bgcolor='white',title_font=dict(size=20, color='darkgreen', family='Arial', weight='bold'),
    title_x=0,
    title_y=0.95,
    xaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'),
    yaxis_title_font=dict(size=16, color='darkgreen', family='Arial', weight='bold'))

feedback_table = dash_table.DataTable(
    id='feedback-table',
    columns=[
        {'name': 'Role', 'id': 'Role'},
        {'name': 'Feedback', 'id': 'Feedback'},
        {'name': 'Sentiment', 'id': 'Sentiment'},
        {'name': 'Sentiment Score', 'id': 'Sentiment Score'}
    ],
    data=df_feedback.to_dict('records'),
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

def feature_2_2():
    return  html.Div([
    html.H1(
        "User Feedback on Trauma-Informed Care Practices",style={'textAlign': 'left', 'marginLeft': '25px', 'color': 'darkgreen'}
    ),
    html.Br(),
    dbc.Row([
        dbc.Col(
            html.Div(
                html.Img(src=wordcloud_image), 
                style={
                    'padding': '20px', 
                    'textAlign': 'center', 
                    'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)', 
                    'borderRadius': '10px', 
                    'backgroundColor': 'white'
                }
            ),
            width=12
        ),
    ], justify="center", style={'marginBottom': '30px'}),
    dbc.Row([
        dbc.Col(
            html.Div(
                dcc.Graph(id='sentiment-pie-chart', figure=fig_pie), 
                style={
                    'padding': '20px', 
                    'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)', 
                    'borderRadius': '10px', 
                    'backgroundColor': 'white'
                }
            ),
            width=4
        ),
        dbc.Col(
            html.Div(
                dcc.Graph(id='sentiment-histogram', figure=fig_hist_sentiment), 
                style={
                    'padding': '20px', 
                    'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)', 
                    'borderRadius': '10px', 
                    'backgroundColor': 'white'
                }
            ),
            width=4
        ),
        dbc.Col(
            html.Div(
                dcc.Graph(id='sentiment-bar-chart', figure=fig_sentiment), 
                style={
                    'padding': '20px', 
                    'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)', 
                    'borderRadius': '10px', 
                    'backgroundColor': 'white'
                }
            ),
            width=4
        ),
    ], justify="center", style={'marginBottom': '30px'}),
    dbc.Row([
        dbc.Col(
            html.Div(
                feedback_table, 
                style={
                    'padding': '20px', 
                    'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)', 
                    'borderRadius': '10px', 
                    'backgroundColor': 'white'
                }
            ),
            width=12
        ),
    ], justify="center"),

], style={'backgroundColor': 'lightgreen', 'padding': '20px','minHeight': '100vh'})

# if __name__ == '__main__':
#     app.run_server(debug=True)
