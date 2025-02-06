import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

event_names = ['Family Therapy', 'Parent Support Group', 'Art Therapy Workshop', 'Family Fun Day', 'Educational Program']
event_types = ['Therapy Session', 'Support Group', 'Workshop', 'Community Activity']
n = 10  

data = {
    'Event Name': np.random.choice(event_names, n),
    'Event Date': pd.date_range(start='2024-01-01', periods=n, freq='7D'),
    'Event Type': np.random.choice(event_types, n),
    'Registered Attendees': np.random.randint(5, 25, n),
    'Event Place': np.random.choice(['Community Center', 'Library', 'Gymnasium', 'Outdoor Park'], n)
}

df_events = pd.DataFrame(data)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def feature_3_2():
    return html.Div([
    html.H1("Engagement Activity Calendar", style={'textAlign': 'left', 'marginLeft': '25px', 'color': 'darkgreen'}),
    html.Div([
        html.H4("Select Event Date Range", style={'textAlign': 'left', 'marginLeft': '25px', 'color': 'darkgreen'}),
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date='2024-01-01',
            end_date='2024-01-10',
            display_format='YYYY-MM-DD',
            style={
                'width': '600px',
                'height': '40px',
                'textAlign': 'center',
                'color': 'darkgreen',
                'borderRadius': '8px',  
                'padding': '8px', 
            },
        ),
    ], style={'textAlign': 'left', 'marginLeft': '25px', 'color': 'darkgreen','marginTop': '20px','borderRadius': '8px'}),
    html.Div([
        html.Div([ 
            html.H4("Event Details", style={'textAlign': 'left', 'marginLeft': '25px', 'color': 'darkgreen'}),
            html.Div(id='event-details', children="Select a date range to see events.", 
                     style={'padding': '20px', 'border': '1px solid #ddd', 'backgroundColor': '#f9f9f9', 'borderRadius': '8px','boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)'})
        ], style={'width': '60%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginRight': '30px'}),
        html.Div([
            html.H4("Event Calendar", style={'textAlign': 'left', 'marginLeft': '25px', 'color': 'darkgreen'}),
            html.Div(id='calendar', children=[], style={'padding': '20px', 'border': '1px solid #ddd', 'backgroundColor': '#f9f9f9', 'borderRadius': '8px','boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)'})
        ], style={'width': '35%', 'display': 'inline-block', 'verticalAlign': 'top'})
    ], style={'marginTop': '30px'})
], style={'backgroundColor': 'lightgreen', 'padding': '20px', 'minHeight': '100vh'}) 

# @app.callback(
#     Output('event-details', 'children'),
#     [Input('date-picker-range', 'start_date'),
#      Input('date-picker-range', 'end_date')]
# )
def display_event_details(start_date, end_date):
    filtered_events = df_events[(df_events['Event Date'] >= start_date) & (df_events['Event Date'] <= end_date)]
    if filtered_events.empty:
        return html.Div("No events found in the selected date range.", style={'color': 'red', 'textAlign': 'center'})
    event_details = []
    for _, event in filtered_events.iterrows():
        event_details.append(
            html.Div([
                html.H5(f"Event Name: {event['Event Name']}", style={
                    'color': 'darkgreen', 'fontWeight': 'bold', 'fontSize': '20px'}),
                html.P(f"Event Type: {event['Event Type']}", style={
                    'fontStyle': 'italic', 'fontSize': '16px', 'color': 'grey'}),
                html.P(f"Registered Attendees: {event['Registered Attendees']}", style={
                    'fontWeight': 'bold', 'fontSize': '16px', 'color': 'blue'}),
                html.P(f"Event Place: {event['Event Place']}", style={
                    'fontSize': '16px', 'color': 'black'}),
                html.Hr(style={'borderTop': '2px solid #4CAF50'})  
            ], style={
                'backgroundColor': '#fff',  
                'padding': '20px',
                'borderRadius': '8px',  
                'border': '1px solid #ddd',  
                'marginBottom': '20px',  
                'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)',  
                'transition': 'all 0.3s ease',  
            })
        )
    return html.Div(event_details)

# @app.callback(
#     Output('calendar', 'children'),
#     [Input('date-picker-range', 'start_date'),
#      Input('date-picker-range', 'end_date')]
# )
def generate_calendar_markers(start_date, end_date):
    filtered_events = df_events[(df_events['Event Date'] >= start_date) & (df_events['Event Date'] <= end_date)]
    markers = []
    for _, event in filtered_events.iterrows():
        markers.append(html.Div(
            children=f"• {event['Event Name']} on {event['Event Date'].strftime('%Y-%m-%d')}",
            style={'padding': '10px', 'border': '1px solid #ddd', 'margin': '12px 0', 'backgroundColor': '#dff0d8', 'borderRadius': '6px', 'cursor': 'pointer', 'fontWeight': 'bold'}
        ))
    
    if not markers:
        markers.append(html.Div("No events in the selected range.", style={'padding': '10px', 'border': '1px solid #ddd'}))
    
    return markers

if __name__ == '__main__':
    app.run_server(debug=True)
