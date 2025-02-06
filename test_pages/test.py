import os
import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from transformers import pipeline
import io
import base64
from dash.exceptions import PreventUpdate
import tempfile
import re
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
import plotly.io as pio
from pages.home import home,plot_two,plot_three,plot_knowledge,generate_graph_report,data_frame_df1,def_2_data_frame,generate_statistical_report

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

generator = pipeline("text-generation", model="gpt2")

df_1= data_frame_df1()
df_2 = def_2_data_frame()

app.layout = html.Div([
    html.H1("Dynamic Report Generation with Hugging Face"),

    plot_two(),
    plot_three(),

    dbc.Button("Generate Report", id='generate-report-btn', color='primary', className="mr-2"),

    html.Div(id='report-text', style={'textAlign': 'justify', 'marginLeft': '50px'}),

    html.Div(id='report-text_1', style={'textAlign': 'justify', 'marginLeft': '50px'}),

    html.A(
        dbc.Button("Download Report", color="success"),
        id="download-link",
        download="report.pdf",
        href="",
        target="_blank"
    ),
])

def clean_text(text):
    """
    Cleans the text by removing non-ASCII characters and unwanted symbols.
    """
    cleaned_text = re.sub(r'[^\x00-\x7F]+', ' ', text)  
    
    cleaned_text = cleaned_text.replace("■", "")  
    
    return cleaned_text

def generate_huggingface_explanation(graph_data):
    
    prompt = f"Analyze the following data frame  and provide a statistical explanation with mean, median and sandhrad deviaion:\n{graph_data}"

    response = generator(prompt, max_new_tokens=100, num_return_sequences=1)

    explanation = response[0]['generated_text']
    return explanation


def generate_pdf_report(figure, explanation,figure_1,explanation_1):
 
    cleaned_explanation = clean_text(explanation)
    cleaned_explanation_1 =clean_text(explanation_1)
    
    buffer = BytesIO()
    img_bytes = pio.to_image(figure, format='png')
    img_bytes_1 = pio.to_image(figure_1, format='png')

    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4  

   
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_img_file:
        temp_img_file.write(img_bytes)
        temp_img_path = temp_img_file.name
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_img_file_1:
        temp_img_file_1.write(img_bytes_1)
        temp_img_path_1 = temp_img_file_1.name
   
    try:
        img_width = 500
        img_height = 300
        img_x = 50  
        img_y = height - 350  
        c.drawString(50, img_y - 20, "Participants in each sector")
        c.drawImage(temp_img_path, img_x, img_y, width=img_width, height=img_height)

        explanation_x = 50
        explanation_y = img_y - 40
        explanation_width = width - 100  
        text_object = c.beginText(explanation_x, explanation_y)
        text_object.setFont("Helvetica", 10)
        text_object.setTextOrigin(explanation_x, explanation_y)

        for line in wrap_text(cleaned_explanation, explanation_width, c):
            text_object.textLine(line)
        c.drawText(text_object)
        
        img_y_1 = img_y - 470  
        c.drawString(50, img_y_1 - 20, "Statistical Overview")
        c.drawImage(temp_img_path_1, img_x, img_y_1, width=img_width, height=img_height)

        explanation_y_1 = img_y_1 - 40
        text_object_1 = c.beginText(explanation_x, explanation_y_1)
        text_object_1.setFont("Helvetica", 10)
        text_object_1.setTextOrigin(explanation_x, explanation_y_1)
        c.showPage()
        for line in wrap_text(cleaned_explanation_1, explanation_width, c):
            text_object_1.textLine(line)
        c.drawText(text_object_1)

        
        c.showPage()
        c.save()

        buffer.seek(0)
        pdf_data = base64.b64encode(buffer.read()).decode('utf-8')
        pdf_link = f"data:application/pdf;base64,{pdf_data}"
        return pdf_link
    finally:
        os.remove(temp_img_path)
        os.remove(temp_img_path_1)

    return pdf_link

def wrap_text(text, width, canvas):
    """
    Wraps the text to fit within a specified width, splitting it into multiple lines.
    """
    lines = []
    current_line = ""
    
    for word in text.split():
        test_line = f"{current_line} {word}".strip()
        if canvas.stringWidth(test_line, "Helvetica", 10) < width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    
    return lines

@app.callback(
    [Output('line-plot', 'figure'),
     Output('report-text', 'children'),
     Output('download-link', 'href'),
     Output('bar-plot', 'figure')],
    Input('generate-report-btn', 'n_clicks'),
    State("line-plot", "figure"),
    State("bar-plot","figure"),
    prevent_initial_call=True
)
def generate_report(n_clicks, figure,figure_1):
    if not n_clicks:
        raise dash.exceptions.PreventUpdate

    if not isinstance(figure, dict) and not isinstance(figure, go.Figure):
        raise ValueError("Expected a Plotly figure, but got a different type.")
    if not isinstance(figure_1, dict) and not isinstance(figure, go.Figure):
        raise ValueError("Expected a Plotly figure, but got a different type.")
    
    explanation = generate_graph_report(df_1)
    explanation_1 = generate_huggingface_explanation(df_2)

    pdf_link = generate_pdf_report(figure, explanation,figure_1,explanation_1)
    combined_explanation = f"Explanation for the first plot:\n{explanation}\n\nExplanation for the second plot:\n{explanation_1}"

    return figure, combined_explanation, pdf_link,figure_1


if __name__ == '__main__':
    app.run_server(debug=True)
