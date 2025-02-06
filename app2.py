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
from features_pages.feature_4_2 import CURD_Operation, add_or_update_data, delete_row, update_dropdown_options, update_graph_db, update_search_results
from features_pages.feature_4_4 import graph_layout, update_graph, update_output
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from flask import Flask, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import time


def encode_image(image_path):
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('ascii')
encoded_image = encode_image("georgia_resilient.png")

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
                        dbc.NavLink("Advanced", href="/advanced",id='advanced-link',className="nav-link-custom"),
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

# app_layout = html.Div([
#     dcc.Location(id='url', refresh=True),
#     html.H2("Welcome to the Dashboard", style={'textAlign': 'center'}),
#     html.Div("You are logged in!"),
#     dbc.Button('Logout', id='logout-button', color='danger', style={'marginTop': '20px'})
# ])

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
            return [html.Div([navbar,home_1_plot(),plot_two(),plot_three(),plot_knowledge(), graph_layout(),CURD_Operation(),footer])], '/home', {'last_path': '/home'}
        elif pathname == "/advanced":
            session['last_path'] = '/advanced'
            print(f"Session Data: {session}")
            print(f'Displaying page adeeb for {last_path}')
            return [html.Div([navbar,issues_overview(),create_expenditure_graph(),footer])], '/advanced', {'last_path': '/advanced'}
        else:
            print(f"Session Data: {session}")
            print(f'Displaying page venky for {last_path}')
            return [html.Div([navbar,home_1_plot(),plot_two(),plot_three(),plot_knowledge(), graph_layout(),footer])], '/home', {'last_path': '/home'}
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
            return [html.Div([navbar,home_1_plot(),plot_two(),plot_three(),plot_knowledge(), graph_layout(),footer])], '', {'logged_in': True, 'last_path': last_path},last_path
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
    [Output('output-data-upload', 'children',allow_duplicate=True),
     Output('graph-output', 'figure',allow_duplicate=True),
     Output('x-axis-dropdown', 'options'),
     Output('y-axis-dropdown', 'options')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')],
    prevent_initial_call=True
)
def update_ouput_in_excel(uploaded_file, filename):
 return update_output(uploaded_file, filename)


@app.callback(
    Output('graph-output', 'figure',allow_duplicate=True),
    [Input('x-axis-dropdown', 'value'),
     Input('y-axis-dropdown', 'value'),
     Input('graph-type-dropdown', 'value')],
    [State('upload-data', 'contents')],
    [State('upload-data', 'filename')],
    prevent_initial_call='initial_duplicate'
)
def update_graph_in_excel(x_col, y_col, graph_type, uploaded_file,filename):
 return update_graph(x_col, y_col, graph_type, uploaded_file,filename)

@app.callback(
    Output('graph', 'figure'),
    [Input('plot-type-dropdown', 'value'),
     Input('df-store', 'data')]  
)

def update_graph_db_connection(plot_type, stored_data):
    return update_graph_db(plot_type, stored_data)

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
     State('df-store', 'data')]  
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
     Output('search-month-dropdown', 'options'),
     Output('update-sector-dropdown', 'options'),
     Output('update-year-dropdown', 'options'),
     Output('update-month-dropdown', 'options')],
    [Input('df-store', 'data')]
)
def update_dropdown_options_db(stored_data):
         return update_dropdown_options(stored_data)

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
if __name__ == '__main__':
    app.run_server(debug=True)
