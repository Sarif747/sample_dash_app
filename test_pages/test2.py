import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import base64
import os
import tempfile

# Initialize Dash app
app = dash.Dash(__name__)

# Generate some sample data
x = [1, 2, 3, 4, 5]
y1 = [2, 3, 4, 5, 6]
y2 = [5, 4, 3, 2, 1]

# Create a few plots
fig1 = go.Figure(data=[go.Scatter(x=x, y=y1, mode='lines', name='Graph 1')])
fig1.update_layout(title="Graph 1: Line Plot")

fig2 = go.Figure(data=[go.Bar(x=x, y=y2, name='Graph 2')])
fig2.update_layout(title="Graph 2: Bar Chart")

# Layout of the Dash App
app.layout = html.Div([
    html.H1("Interactive Dash App with PDF Download", style={'text-align': 'center'}),
    
    dcc.Graph(id='graph1', figure=fig1),
    dcc.Graph(id='graph2', figure=fig2),
    
    html.Button("Download PDF Report", id="download-btn", n_clicks=0),
    
    dcc.Download(id="download-pdf")
])

# Function to generate PDF report
def generate_pdf():
    # Create a PDF file in memory
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Add a title to the PDF
    c.setFont("Helvetica", 16)
    c.drawString(200, 750, "Interactive Graphs Report")

    # Save the graphs as PNG images in memory
    image_data1 = fig1.to_image(format='png')
    image_data2 = fig2.to_image(format='png')
    
    # Create temporary files to store the images
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile1:
        tmpfile1.write(image_data1)
        tmpfile1_path = tmpfile1.name
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile2:
        tmpfile2.write(image_data2)
        tmpfile2_path = tmpfile2.name
    
    # Add the images to the PDF (using the appropriate coordinates)
    c.drawImage(tmpfile1_path, 50, 500, width=400, height=300)
    c.drawImage(tmpfile2_path, 50, 150, width=400, height=300)
    
    # Finalize the PDF
    c.showPage()
    c.save()
    
    # Remove temporary files after use
    os.remove(tmpfile1_path)
    os.remove(tmpfile2_path)
    
    # Return the PDF content
    buffer.seek(0)
    pdf_data = buffer.read()
    return pdf_data

# Callback to handle PDF download
@app.callback(
    Output("download-pdf", "data"),
    Input("download-btn", "n_clicks"),
    prevent_initial_call=True
)
def download_pdf(n_clicks):
    if n_clicks > 0:
        pdf_data = generate_pdf()
        # Ensure the PDF content is encoded correctly in base64
        pdf_base64 = base64.b64encode(pdf_data).decode("utf-8")
        
        # Return the content in the required format for download
        return dict(content=pdf_base64, filename="graphs_report.pdf")
    raise PreventUpdate

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
