import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from flask import Flask, session
import secrets
import dash_bootstrap_components as dbc
import base64
import os
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from dash_bootstrap_components._components.Container import Container
import dash
from flask import Flask
from dash import dcc, html
from pages.home import home,plot_two,plot_three,plot_knowledge
from pages.advance import issues_overview,create_expenditure_graph,expenditure_plot,predict_future
from pages.home_page_1 import home_1_plot,update_map
from features_pages.feature_4_2 import CURD_Operation, add_or_update_data, delete_row, download_file, download_report, update_dropdown_options, update_dropdown_options_2, update_graph_db, update_search_results
from features_pages.feature_4_4 import graph_layout, update_graph, update_graph_types, update_output
from features_pages.feature_4_1 import testing_page_4,display_table,update_training_type_bar,update_knowledge_percent_box,update_duration_distribution,update_correlation_heatmap
from features_pages.feature_4_3 import testing_page_3,upload_file,add_new_data,save_data,download_excel
from features_pages.feature_1 import feature_1,display_county_info,update_table_data,calculate_ace_score
from features_pages.feature_2 import feature_2
from features_pages.feature_3 import feature_3,event_details_display,calendar_markers_generator
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from flask import Flask, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import time

from test_page_feature_4 import data_manipulation, final_submission, search_event_data, show_modal, show_modal_2, submit_data, update_or_delete_data, update_output_2, upload_file_2


server = Flask(__name__)

server.secret_key = secrets.token_hex(24)

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = 'login'  

class User:
    def __init__(self, username, role="user"):
        self.username = username
        self.role = role

    @property
    def is_active(self):
        return True  

    @property
    def is_authenticated(self):
        return True  
    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username
    
    def get_role(self):
        return self.role

    def __repr__(self):
        return f"User(username={self.username}, role={self.role})"


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

app = dash.Dash(__name__, server=server,url_base_pathname='/', external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True,prevent_initial_callbacks='initial_duplicate')

USERS = {
    "admin": {"password": "password123", "role": "admin"},
    "user1": {"password": "mypassword", "role": "user"},
    "user2": {"password": "securepass", "role": "user"}
}

def encode_image(image_path):
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('ascii')
encoded_image = encode_image("georgia_resilient.png")

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='data:image/png;base64,' + encoded_image, height="40px")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://www.resilientga.org/",
                style={"textDecoration": "none"},
            ),
            dbc.Collapse(
               dbc.Nav(
                    [
                        dbc.NavLink("Home", href="/home",id='home-link',className="nav-link-custom"),
                        dbc.DropdownMenu(
                            children=[
                                dbc.DropdownMenuItem("ACE Awareness", href="/ace_awareness", style={'color': 'black', 'display': 'inline-block', 'margin-right': '10px'}),
                                dbc.DropdownMenuItem("Care Analytics", href="/care_analytics", style={'color': 'black', 'display': 'inline-block', 'margin-right': '10px'}),
                                dbc.DropdownMenuItem("Tracking & Support", href="/tracking_support", style={'color': 'black', 'display': 'inline-block'}),
                            ],
                            nav=True,
                            in_navbar=True,
                            label="Features",
                            id="advanced-dropdown",
                            className="nav-link-custom",
                            style={'display': 'inline-block'},  
                            # toggle_style={'display': 'inline-block'},
                            toggle_style={'color': 'black','font-size': '1.1rem'},  
                        ),
                        # dbc.NavLink("Advanced", href="/advanced",id='advanced-link',className="nav-link-custom"),
                        dbc.NavLink("Contact", href="https://www.resilientga.org/contact",id='contact-link',className="nav-link-custom"),
                        dbc.NavLink("Donate", href="https://www.resilientga.org/donate",id='donate-link',className="nav-link-custom"),
                        dbc.Button("Logout",id='logout-button',className="nav-link-custom",style={'backgroundColor': 'lightgreen'}),
                    ],
                    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0", 
                ),
                id="navbar-collapse",
                navbar=True,
            ),
        ]
    ),
    dark=True,
)

footer = html.Div(
    children=[
        html.P(
            children=[
                "© 2024 Your Company Name. All rights reserved. ",
                html.A("Contact Us", href="mailto:contact@example.com",className="atag", style={'color': 'darkgreen','text-decoration':'None'}),
            ],
            style={'textAlign': 'center', 'margin': '10px 0'}
        ),
    ],
    style={'padding': '20px', 'backgroundColor': 'lightgreen', 'borderTop': '1px solid darkgreen'}
)
login_layout = html.Div([
    html.H2("Login to Dashboard",className='lable', style={'textAlign': 'center', 'marginTop': '10px','color': 'darkgreen'}),
    dbc.Row([ 
        dbc.Col([ 
            dbc.Input(id='username', type='text', placeholder='Username',className='input-field',style={
                            'width': '300px',
                            'height': '40px', 
                            'textAlign': 'center',
                            'color': 'darkgreen',
                            'borderRadius': '5px',
                            'border': '1px solid #ccc',
                            'margin': '0 auto',
                            'marginTop': '20px',
                            'marginBottom': '15px', 
                        },),
            dbc.Input(id='password', type='password', placeholder='Password',className='input-field'
                      ,style={
                            'width': '300px',
                            'height': '40px', 
                            'textAlign': 'center',
                            'color': 'darkgreen',
                            'borderRadius': '5px',
                            'border': '1px solid #ccc', 
                            'margin': '0 auto',
                            'marginTop': '20px',
                        }, ),
            dbc.Button('Login', id='login-button', color='primary', className='button',style={
                                    'fontSize': '16px',
                                    'fontWeight': 'bold',
                                    'borderRadius': '5px',
                                    'padding': '10px 20px',
                                    'backgroundColor': 'darkgreen',  
                                    'color': 'white',
                                    'border': 'none',
                                    'cursor': 'pointer',
                                    'transition': 'background-color 0.3s ease',
                                    'textAlign': 'center',   
                                    'width': '100%',  
                                    'maxWidth': '200px',  
                                    'margin': '0 auto',  
                                    'display': 'block', 
                                    'marginTop': '40px', 
                                })
        ], width=12)  
    ], justify='center', style={'padding': '20px'}),  
    html.Div(id='login-error', style={'color': 'red', 'textAlign': 'center', 'marginTop': '10px'}), 
    ], style={
        'boxShadow': '0px 4px 15px rgba(0, 0, 0, 0.9)',
        'borderRadius': '10px',
        'padding': '10px',
        'backgroundColor': 'white',
        'margin': '0',  
        'position': 'absolute',  
        'top': '50%', 
        'left': '50%',  
        'transform': 'translate(-50%, -50%)',  
        'width': '40%',
        'height': '50%' 
    })

# app_layout
app_layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content', className='mt-4'),  
], fluid=True)

app.layout = html.Div([
    dcc.Store(id='session-store', storage_type='session'),  
    dcc.Location(id='url', refresh=False),  
    html.Div(id='page-content', children=login_layout), 
])

@app.callback(
    [Output('page-content', 'children'),
     Output('url', 'pathname'),
     Output('session-store', 'data')],
    [Input('url', 'pathname')],
    prevent_initial_call=True
)

def display_page(pathname):
    if 'user' in session:   
        last_path = session.get('last_path', '/home')  
        print(f'Displaying page arbazz for {last_path}')
        if pathname == "/home":
            session['last_path'] = '/home'
            print(f"Session Data: {session}")
            print(f'Displaying page arif for {last_path}')
            if session.get('role') == 'admin':
                return [html.Div([navbar,data_manipulation(),testing_page_4(),CURD_Operation(),testing_page_3(),graph_layout(),footer])], '/home', {'last_path': '/home'}
            else:
                return [html.Div([navbar,testing_page_4(),CURD_Operation(),testing_page_3(),graph_layout(),footer])], '/home', {'last_path': '/home'}
        elif pathname == "/ace_awareness":
            session['last_path'] = '/ace_awareness'
            print(f"Session Data: {session}")
            print(f'Displaying page adeeb for {last_path}')
            return [html.Div([navbar,feature_1(),footer])], '/ace_awareness', {'last_path': '/ace_awareness'}
        elif pathname == "/care_analytics":
            session['last_path'] = '/care_analytics'
            print(f"Session Data: {session}")
            print(f'Displaying page adeeb for {last_path}')
            return [html.Div([navbar,feature_2(),footer])], '/care_analytics', {'last_path': '/care_analytics'}
        elif pathname == "/tracking_support":
            session['last_path'] = '/tracking_support'
            print(f"Session Data: {session}")
            print(f'Displaying page adeeb for {last_path}')
            return [html.Div([navbar,feature_3(),footer])], '/tracking_support', {'last_path': '/tracking_support'}
        else:
            print(f"Session Data: {session}")
            print(f'Displaying page venky for {last_path}')
            return [html.Div([navbar,testing_page_4(),CURD_Operation(),testing_page_3(),graph_layout(),footer])], '/home', {'last_path': '/home'}
    else:
        return [login_layout],'/', {'logged_in': False, 'last_path': '/home'}

@app.callback(
    [Output('page-content', 'children',allow_duplicate=True),
     Output('login-error', 'children'),
     Output('session-store', 'data',allow_duplicate=True),
     Output('url', 'pathname',allow_duplicate=True)],
    [Input('login-button', 'n_clicks')],
    [State('username', 'value'),
     State('password', 'value')],
    prevent_initial_call=True
)
def handle_login(n_clicks, username, password):
    if n_clicks:
        if username in USERS and USERS[username]['password'] == password:
            user = User(username)
            login_user(user)
            session['user'] = username
            session['role'] = USERS[username]['role']
            last_path = session.get('last_path', '/home')
            print(f'Login successful, redirecting to {last_path}')
            session['last_path'] = last_path
            time.sleep(5)
            if session.get('role') == 'admin':
                return [html.Div([navbar,data_manipulation(),testing_page_4(),CURD_Operation(),testing_page_3(),graph_layout(),footer])], '', {'logged_in': True, 'last_path': last_path},last_path
            return [html.Div([navbar,testing_page_4(),CURD_Operation(),testing_page_3(),graph_layout(),footer])], '', {'logged_in': True, 'last_path': last_path},last_path
        else:
            last_path = '/'
            return [login_layout], 'Invalid username or password',{'logged_in': True, 'last_path': '/home'},last_path
    last_path = ''
    return [login_layout],'',{'logged_in': False, 'last_path': '/'},last_path

@app.callback(
    [Output('page-content', 'children',allow_duplicate=True),
     Output('url', 'pathname',allow_duplicate=True),
     Output('session-store', 'data',allow_duplicate=True)],
    [Input('logout-button', 'n_clicks')],
    prevent_initial_call=True
)   

def handle_logout(n_clicks):
    if n_clicks:
        logout_user()
        session.pop('user',None)
        current_path = session.get('last_path', '/home')
        session['last_path'] = current_path  
        return [login_layout], '/', {'logged_in': False, 'last_path': current_path}
    last_path = session.get('last_path', '/home')
    print(f"Session Data: {session}")
    print(f'logout successful, redirecting to {last_path}')
    return dash.no_update, last_path, {'logged_in': True, 'last_path': '/home'}


@app.callback(
    Output('prediction-output', 'children'),
    Output('expenditure-plot', 'figure'),
    Input('predict-button', 'n_clicks'),
    Input('year-dropdown-predict', 'value'),
    Input('year-slider', 'value'),  
    Input('show-all-checkbox', 'value')
)
def update_prediction(n_clicks, prediction_year, selected_year, show_all):
    if n_clicks > 0:
        predictions = predict_future(prediction_year)
        prediction_text = "\n".join([f"{category}: ${value:.2f}" for category, value in predictions.items()])
        
        fig_expenditures = expenditure_plot(selected_year, show_all, predictions)
        
        return f"Predicted Expenditures for {prediction_year}:\n{prediction_text}", fig_expenditures
    return "", expenditure_plot(selected_year, show_all,predicted_values={})

@app.callback(
    Output('map-graph', 'figure'),
    Input('training-type-dropdown', 'value')
)
def show_home_plot_graph(selected_training_type):
    return update_map(selected_training_type)
    
@app.callback(
    [Output('output-data-upload', 'children', allow_duplicate=True),
     Output('graph-output', 'children', allow_duplicate=True),
     Output('axis-dropdown', 'options')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_ouput_in_excel(uploaded_file, filename):
 return update_output(uploaded_file, filename)

@app.callback(
    Output('graph-type-dropdown', 'options'),
    Output('graph-type-dropdown', 'placeholder'),
    Input('axis-dropdown', 'value')
)
def update_graphTypes(selected_columns):
     return update_graph_types(selected_columns)

@app.callback(
    Output('graph-output', 'children', allow_duplicate=True),
    [Input('axis-dropdown', 'value'),
     Input('graph-type-dropdown', 'value')],
    [State('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_graph_in_excel(axis_col, graph_types, uploaded_file,filename):
 return update_graph(axis_col, graph_types, uploaded_file,filename)

@app.callback(
    Output('graphs-container', 'children'),
    [Input('df-store', 'data')] 
)

def update_graph_db_connection(stored_data):
    return update_graph_db(stored_data)

@app.callback(
    [Output('df-store', 'data'),
     Output('output_message','children')], 
    [Input('add-button', 'n_clicks'),
     Input('update-button', 'n_clicks')],
    [State('add-sector-input', 'value'),
     State('add-year-input', 'value'),
     State('add-month-input', 'value'),
     State('add-participants-input', 'value'),
     State('update-sector-dropdown', 'value'),
     State('update-year-dropdown', 'value'),
     State('update-month-dropdown', 'value'),
     State('update-participants', 'value'),
     State('df-store', 'data')],  
     prevent_initial_call=True
)
def add_update_data(add_clicks, update_clicks, add_sector, add_year, add_month, add_num_participants,
                       update_sector, update_year, update_month, update_num_participants, stored_data):
        if session.get('role') == 'admin':
            return add_or_update_data(add_clicks, update_clicks, add_sector, add_year, add_month, add_num_participants,
                        update_sector, update_year, update_month, update_num_participants, stored_data)
        else:
            return '','You do not have permission'


@app.callback(
    Output('search-results-table', 'data',allow_duplicate=True),
    [Input('search-sector-dropdown', 'value'),
     Input('search-year-dropdown', 'value'),
     Input('search-month-dropdown', 'value'),
     Input('df-store', 'data')]  
)
def update_search_results_db(sector, year, month, stored_data):
        return update_search_results(sector, year, month, stored_data)

@app.callback(
    [Output('search-sector-dropdown', 'options'),
     Output('search-year-dropdown', 'options'),
     Output('search-month-dropdown', 'options')],
    [Input('df-store', 'data')],
    prevent_initial_call=True
)
def update_dropdown_options_db(stored_data):
         return update_dropdown_options(stored_data)

@app.callback(
    [Output('update-sector-dropdown', 'options'),
     Output('update-year-dropdown', 'options'),
     Output('update-month-dropdown', 'options')],
    [Input('df-store', 'data')],
    prevent_initial_call=True
)
def update_dropdown_options_db2(stored_data):
    return update_dropdown_options_2(stored_data)

@app.callback(
    [Output('search-results-table', 'data',allow_duplicate=True),
     Output('df-store', 'data',allow_duplicate=True)],
    [Input('search-results-table', 'data_previous')],
    [State('search-results-table', 'data'),
     State('df-store', 'data')]
)
def delete_row_db(data_previous, current_data, stored_data): 
        print("role check")
        print(session.get('role'))
        if session.get('role') == 'admin':
            return delete_row(data_previous, current_data, stored_data)
        else:
            return current_data, stored_data

@app.callback(
    Output('download-link-container', 'children',allow_duplicate=True),
    #  Output('download-link-store', 'data')],
    [Input('download-button_report', 'n_clicks')],
    # [State('download-link-store', 'data')]
)
def report_downlode(n_clicks):
     print("clicked on genrate report to display link")
     return download_report(n_clicks)

# @app.callback(
#     Output('download-link-container', 'children',allow_duplicate=True),
#     [Input('download-link-store', 'data')]
# )
# def render_link_download(data):
#     return render_download_link(data)

@app.server.route('/download/<filename>')
def file_download(filename):
     print("clicked on download link")
     return download_file(filename)

@app.callback(
    Output('data-table', 'data'),
    Output('data-table', 'columns'),
    Input('county-dropdown', 'value')
)
def table_display(selected_counties):
    return display_table(selected_counties)

@app.callback(
    Output('training-type-bar', 'figure'),
    Input('county-dropdown', 'value')
)
def training_type_bar(selected_counties):
    return update_training_type_bar(selected_counties)

@app.callback(
    Output('knowledge-percent-box', 'figure'),
    Input('county-dropdown', 'value')
)
def knowledge_percent_box(selected_counties):
    return update_knowledge_percent_box(selected_counties)

@app.callback(
    Output('duration-distribution', 'figure'),
    Input('county-dropdown', 'value')
)
def duration_distribution(selected_counties):
    return update_duration_distribution(selected_counties)
   
@app.callback(
    Output('correlation-heatmap', 'figure'),
    Input('county-dropdown', 'value')
)
def correlation_heatmap(selected_counties):
    return update_correlation_heatmap(selected_counties)

@app.callback(
    Output('file-data-table', 'children',allow_duplicate=True),
    Output('input-fields', 'children'),
    Output('dynamic-buttons', 'children',allow_duplicate=True),  
    Input('upload-data_1', 'contents'),
    State('upload-data_1', 'filename'),
)
def file_upload_file(contents, filename):
     return upload_file(contents, filename)
     
@app.callback(
    Output('file-data-table', 'children'),
    Output('save-data-message', 'children',allow_duplicate=True),
    Input('add-new-data-button', 'n_clicks'),
    State('uploaded-data-table', 'data'),
    State('uploaded-data-table', 'columns'),
    State('input-fields', 'children'),
)
def new_data_add(n_clicks, data, columns, input_fields):
    return add_new_data(n_clicks, data, columns, input_fields)

@app.callback(
    Output('save-data-message', 'children'),
    Output('dynamic-buttons', 'children'), 
    Input('save-data-button', 'n_clicks'),
    State('uploaded-data-table', 'data'),
    State('uploaded-data-table', 'columns')
)
def data_save(n_clicks, data, columns):
    return save_data(n_clicks, data, columns)

@app.callback(
    Output('download-data', 'data'),
    Input('download-button', 'n_clicks'),
)
def excel_download(n_clicks):
    return download_excel(n_clicks)

@app.callback(
    [Output('county-info', 'children'),
     Output('county-table', 'data')],
    [Input('map-graph', 'hoverData')]
)
def county_info_display(hoverData):
    return display_county_info(hoverData)

@app.callback(
    Output('county-table', 'data', allow_duplicate=True),
    [Input('county-table', 'data_previous')],
    [State('county-table', 'data')]
)
def table_data_update(data_previous, data):
    return update_table_data(data_previous, data)

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

@app.callback(
    [Output('result', 'children'),
     Output('resources', 'style'),
     Output('resource-link', 'children')],
    Input('calculate-btn', 'n_clicks'),
    [Input(f"q{i+1}", 'value') for i in range(len(questions))]
)
def ace_score_calculate(n_clicks, *answers):
    return calculate_ace_score(n_clicks, *answers)

@app.callback(
    Output('event-details', 'children'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def event_detailsDisplay(start_date, end_date):
    return event_details_display(start_date, end_date)

@app.callback(
    Output('calendar', 'children'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def calendar_markersGenerator(start_date, end_date):
    return calendar_markers_generator(start_date, end_date)


@app.callback(
    Output('data-table-container', 'children', allow_duplicate=True),
    Output('output-data-upload', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    prevent_initial_call=True
)
def upload_file_3(contents, filename):
    return upload_file_2(contents,filename)

@app.callback(
    Output("modal-container", "children"),
    Output("modal-state", "data", allow_duplicate=True),
    Input("submit-button", "n_clicks"),
    State('upload-data', 'contents'),
    State('data-table-container', 'children'),
    prevent_initial_call=True
)
def show_modal_4(n_clicks,contents, table):
    return show_modal(n_clicks,contents, table)

@app.callback(
    Output('final-submission', 'children'),
    Output("modal-state", "data", allow_duplicate=True),
    Input("confirm-submit-button", "n_clicks"),
    State('data-table-container', 'children'), 
    prevent_initial_call=True
)
def final_submission_2(n_clicks, table):
    return final_submission(n_clicks, table)

@app.callback(
    [Output('modal-container_2', 'children'),
     Output('modal-state_2', 'data')],
    Input('submit-form-button', 'n_clicks'),
    [State('event-name', 'value'),
     State('county', 'value'),
     State('address', 'value'),
     State('population-served', 'value'),
     State('event-type', 'value'),
     State('number-trained', 'value'),
     State('hours', 'value'),
     State('event-date', 'value'),
     State('demographic-info', 'value'),
     State('identified-gaps', 'value'),],
    prevent_initial_call=True
)
def show_modal_3(n_clicks,event_name, county, address, population_served, event_type, number_trained, hours, event_date, demographic_info, identified_gaps):
    return show_modal_2(n_clicks,event_name, county, address, population_served, event_type, number_trained, hours, event_date, demographic_info, identified_gaps)

@app.callback(
    Output('output-data-upload_1', 'children'),
    Input('confirm-submit-button-2', 'n_clicks'),
    [State('event-name', 'value'),
     State('county', 'value'),
     State('address', 'value'),
     State('population-served', 'value'),
     State('event-type', 'value'),
     State('number-trained', 'value'),
     State('hours', 'value'),
     State('event-date', 'value'),
     State('demographic-info', 'value'),
     State('identified-gaps', 'value'),
     State('modal-state_2', 'data')]
)
def submit_data_2(confirm_clicks, event_name, county, address, population_served, event_type, number_trained, hours, event_date, demographic_info, identified_gaps, modal_state):
    return submit_data(confirm_clicks, event_name, county, address, population_served, event_type, number_trained, hours, event_date, demographic_info, identified_gaps, modal_state)

@app.callback(
    Output('search-results-container', 'children'),
    Output('search-output', 'children'),
    Input('search-event-name', 'value'),
    Input('search-event-date', 'value')
)
def search_event_data_2(event_name, event_date):
    return search_event_data(event_name, event_date)

@app.callback(
    Output("update-feedback", "children"),
    Input("search-results-table", "data"),
    State("search-results-table", "data_previous"),
)
def update_or_delete_data_2(current_data, previous_data):
    return update_or_delete_data(current_data, previous_data)

@app.callback(
    [Output('sql-output', 'children'),
     Output('query-result', 'children')],
    Input('convert-button', 'n_clicks'),
    [Input('user-input', 'value')]
)
def update_output_3(n_clicks, user_input):
    return update_output_2(n_clicks, user_input)

if __name__ == '__main__':
    app.run_server(debug=True)