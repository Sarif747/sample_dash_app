import numpy as np
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html

def generate_synthetic_knowledge_data(num_entries):
    categories = [
        "Understanding of Trauma",
        "Understanding of Resiliency",
        "Regional Connectivity",
        "Enhanced Strategies",
        "Tangible Next Steps"
    ]
    
    synthetic_data = {
        "Category": categories,
        "Pre-Survey": np.random.uniform(50, 60, len(categories)).tolist(),
        "Post-Survey": np.random.uniform(65, 75, len(categories)).tolist(),
    }
    
    synthetic_data["Increase (%)"] = [
        ((post - pre) / pre) * 100 for pre, post in zip(synthetic_data["Pre-Survey"], synthetic_data["Post-Survey"])
    ]

    return pd.DataFrame(synthetic_data)

synthetic_knowledge_df = generate_synthetic_knowledge_data(5)

heatmap_data = synthetic_knowledge_df.set_index('Category')[['Pre-Survey', 'Post-Survey']]

app = dash.Dash(__name__)

fig_heatmap = px.imshow(
    heatmap_data.T,  
    labels=dict(x="Category", y="Survey Type", color="Score"),
    x=heatmap_data.index,
    y=['Pre-Survey', 'Post-Survey'],
    color_continuous_scale='Greens',
    title='Heatmap of Knowledge Assessment Scores'
)

app.layout = html.Div([
    html.H1("Knowledge Assessment Dashboard", style={'textAlign': 'center'}),
    dcc.Graph(
        id='heatmap',
        figure=fig_heatmap
    )
], style={'backgroundColor': 'lightgrey', 'padding': '20px'})

if __name__ == '__main__':
    app.run_server(debug=True)
