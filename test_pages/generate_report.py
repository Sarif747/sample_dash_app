from email import generator
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.io as pio
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import base64
from pages.home import home,plot_two,plot_three,plot_knowledge
from pages.advance import issues_overview,create_expenditure_graph,expenditure_plot,predict_future
# from pages.excel import graph_layout, update_graph, update_output
import dash_bootstrap_components as dbc
from flask import Flask
from reportlab.pdfgen import canvas
import base64
from PIL import Image
import tempfile
import os
import shutil

server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# home_1_plot(),plot_two(),plot_three(),plot_knowledge(), graph_layout(),issues_overview(),create_expenditure_graph()

app.layout = html.Div([
    html.H1("Generate and Download Report"),
    plot_two(), 
    html.Button("Generate Report", id="generate-report-button", n_clicks=0),
    html.Div(id="report-output") 
])

@app.callback(
    Output("report-output", "children"),
    Input("generate-report-button", "n_clicks"),
    State("line-plot", "figure")  
)

def generate_report(n_clicks, figure):
    print(f"Button clicked {n_clicks} times.") 
    
    image_path = 'plot_screenshot.png'
    pio.write_image(figure, image_path)
    prompt = f"Analyze the following graph data and provide statistical details:\n{figure}"
    stats_explanation = generator(prompt, max_length=150)[0]['generated_text']
    if n_clicks > 0:
        pdf_buffer = BytesIO()
        c = canvas.Canvas(pdf_buffer)
        c.setFont("Helvetica", 14)
        c.drawString(100, 750, "Sample Report - Plotly Graph")
        img_bytes = pio.to_image(figure, format="png")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
            tmp_file.write(img_bytes) 
            tmp_file_path = tmp_file.name
        c.drawImage(tmp_file_path, 50, 500, width=500, height=300)
        c.write(stats_explanation)
        c.save()
        pdf_buffer.seek(0)
        pdf_base64 = base64.b64encode(pdf_buffer.read()).decode("utf-8")
        pdf_data = f"data:application/pdf;base64,{pdf_base64}"
        os.remove(tmp_file_path)
        return html.A("Download PDF Report", href=pdf_data, download="report.pdf")
    return html.Div()

if __name__ == '__main__':
    app.run_server(debug=True)
