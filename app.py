import base64
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from dash_bootstrap_components._components.Container import Container
import dash
from dash import dcc, html
from pages.home import home,plot_two,plot_three,plot_knowledge
from pages.advance import issues_overview,create_expenditure_graph,expenditure_plot,predict_future
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def encode_image(image_path):
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('ascii')

encoded_image = encode_image(r'F:\sample_dash_app\assets\Resilient.png')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP,"assets/styles.css"],suppress_callback_exceptions=True)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='data:image/png;base64,' + encoded_image, height="30px")),
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
                        dbc.NavLink("Home", href="#home",active="exact",id='home-link',className="nav-link-custom"),
                        dbc.NavLink("Advanced", href="#advanced",active="exact",id='advanced-link',className="nav-link-custom"),
                        dbc.NavLink("Contact", href="https://www.resilientga.org/contact",active="exact",id='contact-link',className="nav-link-custom"),
                        dbc.NavLink("Donate", href="https://www.resilientga.org/donate",active="exact",id='donate-link',className="nav-link-custom"),
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

app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='content', className='mt-4'),  
], fluid=True)

@app.callback(
    Output('content', 'children'),
    Output('home-link', 'className'),
    Output('advanced-link', 'className'),
    Output('contact-link', 'className'),
    Output('donate-link', 'className'),
    Input('url', 'hash')
)

def display_page(hash):
    home_class = 'nav-link-custom'
    advanced_class = 'nav-link-custom'
    contact_class = 'nav-link-custom'
    donate_class = 'nav-link-custom'
    if hash == "#advanced":
        advanced_class += ' active'
        return (html.Div([issues_overview(),create_expenditure_graph(),footer
        ]), home_class, advanced_class, contact_class, donate_class)
    # elif hash == "#contact":
    #     contact_class += ' active'
    #     return (html.Div([
    #         html.H2("Contact Us"),
    #         html.P("You can contact us at contact@example.com.")
    #     ]),home_class, advanced_class, contact_class, donate_class)
    # elif hash == "#donate":
    #     donate_class += ' active'
    #     return (html.Div([
    #         html.H2("Donate Us"),
    #         html.P("Support us by donating!")
    #     ]),home_class, advanced_class, contact_class, donate_class)
    else: 
        home_class += ' active'
        return (html.Div([home(),plot_two(),plot_three(),plot_knowledge(),footer]), home_class, advanced_class, contact_class, donate_class)
    
# @app.callback(
#     Output('expenditure-plot', 'figure'),
#     Input('year-slider', 'value'),
#     Input('show-all-checkbox', 'value'),
# )
# def update_expenditure_plot(selected_year,show_all,predicted_values=None):
#     return expenditure_plot(selected_year,show_all,predicted_values=None)

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


if __name__ == '__main__':
    app.run_server(debug=True)