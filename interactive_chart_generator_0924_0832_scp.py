# 代码生成时间: 2025-09-24 08:32:19
import os
import json
from celery import Celery
from flask import Flask, request, jsonify
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from bokeh.models import HoverTool

# Initialize Celery
app = Flask(__name__)
celery_app = Celery(__name__)
celerynos = os.getenv("CELERY_BROKER_URL")
if celerynos:
    celery_app.conf.broker_url = celerynos

# Define a task for generating interactive charts using Celery
@celery_app.task
def generate_chart(data):
    """Generates an interactive chart based on provided data.
    
    Args:
        data (dict): A dictionary containing chart configuration and data.
    
    Returns:
        dict: A dictionary containing chart HTML and script components.
    """
    try:
        # Create a new plot
        p = figure(title=data['title'], x_axis_label=data['x_axis_label'], y_axis_label=data['y_axis_label'])
        
        # Add data to the plot
        p.line(data['x'], data['y'], legend_label=data.get('legend_label'))
        
        # Add hover tool
        p.add_tools(HoverTool(tooltips=[("x", "@x"), ("y", "@y")]))
        
        # Generate HTML and script components
        html, script = components(p)
        
        # Save plot to HTML file
        output_file(os.path.join('plots', data['filename'] + '.html'), p)
        
        return {'html': html, 'script': script}
    except Exception as e:
        # Handle any errors that occur during chart generation
        return {'error': str(e)}

# Flask route to trigger chart generation
@app.route('/generate_chart', methods=['POST'])
def generate_chart_route():
    """Receives chart data via POST request and returns generated chart components."""
    if request.method == 'POST':
        try:
            # Load JSON data from request
            data = request.get_json()
            
            # Call Celery task to generate chart
            result = generate_chart.delay(data)
            
            # Wait for task completion and return results
            return jsonify(result.get())
        except Exception as e:
            # Handle any errors that occur during request handling
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'error': 'Invalid request method'}), 405

if __name__ == '__main__':
    # Run Flask app
    app.run(debug=True)